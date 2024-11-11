# ganzithon/blog/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.shortcuts import get_object_or_404
from .models import Blog, Comment
from .serializers import BlogSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import AuthenticationFailed

# 전체 게시글 목록 조회 및 게시글 작성
class BlogList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            raise AuthenticationFailed({"detail": "Authentication credentials were not provided."})

        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 특정 게시글 조회, 수정, 삭제
class BlogDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny] 

    def get_object(self, post_id):
        return get_object_or_404(Blog, pk=post_id)

    def get(self, request, post_id):
        blog = self.get_object(post_id)
        serializer = BlogSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, post_id):
        if not request.user.is_authenticated:
            raise AuthenticationFailed({"detail": "Authentication credentials were not provided."})

        blog = self.get_object(post_id)
        self.check_object_permissions(request, blog)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        if not request.user.is_authenticated:
            raise AuthenticationFailed({"detail": "Authentication credentials were not provided."})

        blog = self.get_object(post_id)
        self.check_object_permissions(request, blog)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 특정 게시글 댓글 조회 및 작성
class CommentList(APIView):
    permission_classes = [AllowAny]  

    def get(self, request, post_id):
        blog = get_object_or_404(Blog, pk=post_id)
        comments = blog.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        if not request.user.is_authenticated:
            raise AuthenticationFailed({"detail": "Authentication credentials were not provided."})

        blog = get_object_or_404(Blog, pk=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, blog=blog)
            blog_serializer = BlogSerializer(blog)
            return Response(blog_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 특정 게시글 댓글 삭제 
class CommentDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, post_id, comment_id):
        return get_object_or_404(Comment, pk=comment_id, blog_id=post_id)

    def delete(self, request, post_id, comment_id):
        if not request.user.is_authenticated:
            raise AuthenticationFailed({"detail": "Authentication credentials were not provided."})

        comment = self.get_object(post_id, comment_id)
        self.check_object_permissions(request, comment)
        comment.delete()
        blog = get_object_or_404(Blog, pk=post_id)
        blog_serializer = BlogSerializer(blog)
        return Response(blog_serializer.data, status=status.HTTP_200_OK)
