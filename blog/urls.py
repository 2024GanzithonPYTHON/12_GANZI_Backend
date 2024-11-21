# ganzithon/blog/urls.py
from django.urls import path
from .views import BlogList, BlogDetail, CommentList, CommentDetail, UserBlogList

app_name = 'blog'

urlpatterns = [
    path('', BlogList.as_view(), name='blog_list'), # 커뮤니티 전체 게시글 목록 조회 / 커뮤니티 게시글 작성 
    path('<int:post_id>/', BlogDetail.as_view(), name='blog_detail'), # 커뮤니티 특정 게시글 조회 / 수정 / 삭제
    path('<int:post_id>/comment/', CommentList.as_view(), name='comment_list'), # 커뮤니티 특정 게시글의 전체 댓글 조회 / 커뮤니티 특정 게시글에 댓글 작성
    path('<int:post_id>/comment/<int:comment_id>/', CommentDetail.as_view(), name='comment_detail'), # 커뮤니티 특정 게시글에 댓글 삭제
    path('my-posts/', UserBlogList.as_view(), name='user_blog_list'),  # 사용자 작성 글 조회
]
