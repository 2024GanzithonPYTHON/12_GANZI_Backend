# ganzithon/purchase/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import PurchasePost, PurchaseApplication
from .serializers import PurchasePostSerializer, PurchaseApplicationSerializer


# 공동 구매 게시글 생성
class PurchasePostView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk=None):
        # 전체 게시글 조회
        if pk is None:
            posts = PurchasePost.objects.all()  # 모든 게시글 조회

            serializer = PurchasePostSerializer(posts, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        # 특정 게시글 조회
        post = get_object_or_404(PurchasePost, pk=pk)

        # 공동 구매 기간 종료 확인
        if post.duration <= timezone.now():
            return Response(
                {"detail": "This post is no longer accessible because the duration has ended."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 작성자 여부 확인
        is_author = request.user == post.user

        # 시리얼라이저에 작성자 여부 전달
        serializer = PurchasePostSerializer(post,context={'request': request, 'is_author': is_author})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PurchasePostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        post = get_object_or_404(PurchasePost, pk=pk)

        # 작성자만 수정 가능
        if request.user != post.user:
            return Response({"detail": "You do not have permission to edit this post."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = PurchasePostSerializer(post, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(PurchasePost, pk=pk)

        # 작성자만 삭제 가능
        if request.user != post.user:
            return Response({"detail": "You do not have permission to delete this post."},
                            status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({"detail": "Post deleted successfully."}, status=status.HTTP_200_OK)


# 공동 구매 신청 관리
class ApplyToPurchaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # 신청할 게시글 가져오기
        post = get_object_or_404(PurchasePost, pk=pk)


        # 중복 신청 확인
        if PurchaseApplication.objects.filter(post=post, user=request.user).exists():
            return Response({"detail": "You have already applied to this post."},
                            status=status.HTTP_400_BAD_REQUEST)

        # 사용자 정보 가져오기
        user = request.user
        email = user.email
        address = f"{user.postal_code}, {user.city}, {user.address1}, {user.address2 or ''}".strip(', ')
        nickname = user.nickname

        # 신청 내역 저장
        application = PurchaseApplication.objects.create(
            post=post,
            user=user,
            email=email,
            address=address,
            nickname=nickname
        )

        # 확인을 위한 로그
        print(f"Application created: {application}")  # 콘솔에 로그 출력
        return Response({"detail": "Application successful.", "application_id": application.id},
                        status=status.HTTP_201_CREATED)

class UserApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 현재 사용자와 관련된 모든 신청 내역 가져오기
        applications = PurchaseApplication.objects.filter(user=request.user).select_related('post')

        # 시리얼라이저를 사용하여 데이터 직렬화
        serializer = PurchaseApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)