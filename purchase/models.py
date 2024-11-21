# ganzithon/purchase/models.py
from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from datetime import datetime


class PurchasePost:
    pass


class PurchasePost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.URLField(null=True, blank=True)  # 이미지 URL을 위한 필드
    tags = models.JSONField(null=True, blank=True)  # 선택 사항: JSON 형식으로 태그 저장
    body = models.TextField()
    email_subject = models.CharField(max_length=100)
    email_body = models.TextField()
    payment_period = models.DateField()
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=200)
    duration_date = models.DateField()
    duration_time = models.TimeField()
    min_participants = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    open = models.BooleanField(default=True)  # 게시글 상태 (열림/닫힘)

    def close_if_expired(self):
        """마감 기한이 지나면 게시글을 닫음"""
        if self.duration_date < timezone.now().date() and self.open:
            self.open = False
            self.save()

    def __str__(self):
        return self.title

    @property
    def duration(self):
        combined_datetime = datetime.combine(self.duration_date, self.duration_time)
        return timezone.make_aware(combined_datetime, timezone.get_current_timezone())

class PurchaseApplication(models.Model):
    post = models.ForeignKey(PurchasePost, on_delete=models.CASCADE, related_name='applications')  # 신청한 게시글
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 신청자
    email = models.EmailField()  # 신청자의 이메일 (회원 가입 정보에서 가져옴)
    address = models.CharField(max_length=200)  # 신청자의 주소 (회원 가입 정보에서 가져옴)
    nickname = models.CharField(max_length=100)  # 신청자의 닉네임 (회원 가입 정보에서 가져옴)

    def __str__(self):
        return f"{self.nickname} applied to {self.post.title}"
