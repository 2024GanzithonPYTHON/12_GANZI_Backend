# ganzithon/purchase/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import PurchasePost

@shared_task
def check_and_send_emails():
    # 현재 시간을 기준으로 만료된 게시글 필터링
    now = timezone.now()
    expired_posts = PurchasePost.objects.filter(
        duration_date__lte=now.date(),
        duration_time__lte=now.time(),
        min_participants__gt=0
    )

    for post in expired_posts:
        # 공동 구매 신청자 수 확인
        if post.participant_set.count() >= post.min_participants:
            # 이메일 구성
            subject = f"[공동구매 완료 안내] {post.email_subject}"
            body = (
                f"안녕하세요, 공동 구매에 참여해 주셔서 감사합니다!\n\n"
                f"공동 구매 제목: {post.title}\n"
                f"공동 구매 내용: {post.body}\n"
                f"\n결제 및 배송 정보를 준비해 주세요:\n"
                f"- 결제 기한: {post.payment_period}\n"
                f"- 은행명 및 계좌번호: {post.bank_name} - {post.account_number}\n"
                f"- 문의 연락처: {post.contact_info}\n"
                f"\n빠른 결제 부탁드리며, 문의 사항이 있으시면 언제든지 연락해 주세요."
            )
            
            # 신청자 이메일 목록 생성
            email_list = [participant.user.email for participant in post.participant_set.all()]

            # 이메일 발송
            send_mail(
                subject,
                body,
                'admin@ganzithon.com',  # 발신자 이메일 주소
                email_list,
                fail_silently=False,
            )

        # 공동 구매 기간이 종료된 게시글 업데이트
        post.min_participants = 0
        post.save()
