# ganzithon/blog/views.py
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Blog, Comment
from .serializers import BlogSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import AuthenticationFailed

# 전체 게시글 목록 조회 및 게시글 작성
class BlogList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly] # 인증된 사용자만 접근 가능

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


class UserBlogList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request):
        # 현재 사용자와 관련된 게시글 필터링
        user_blogs = Blog.objects.filter(user=request.user)

        # 검색 필터 추가
        search_query = request.query_params.get('search', None)
        if search_query:
            user_blogs = user_blogs.filter(
                title__icontains=search_query
            ) | user_blogs.filter(
                body__icontains=search_query
            )

        # 최신 날짜 순 정렬
        user_blogs = user_blogs.order_by('-date')

        # Pagination 조건 확인
        all_data = request.query_params.get('all', 'false').lower() == 'true'
        if all_data:
            serializer = BlogSerializer(user_blogs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Pagination 적용
        paginator = PageNumberPagination()
        paginator.page_size = 100  # 한 페이지에 최대 100개씩 반환
        result_page = paginator.paginate_queryset(user_blogs, request)

        serializer = BlogSerializer(user_blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)