# ganzithon/purchase/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import PurchasePost
from .serializers import PurchasePostSerializer

# 공동 구매 게시글 생성
class PurchasePostView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk=None):
        post = get_object_or_404(PurchasePost, pk=pk)

        # 공동 구매 기간 종료 확인
        if post.duration <= timezone.now():
            return Response(
                {"detail": "This post is no longer accessible because the duration has ended."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PurchasePostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PurchasePostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
