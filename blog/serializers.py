# ganzithon/blog/serializers.py
from rest_framework import serializers
from .models import Blog, Comment

# 댓글 시리얼라이저 
class CommentSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    date = serializers.SerializerMethodField()  

    class Meta:
        model = Comment
        fields = ['id', 'user', 'nickname', 'comment', 'date']

    def get_date(self, obj):
        return obj.date.strftime("%Y-%m-%d")  

# 커뮤니티 게시글 시리얼라이저 
class BlogSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    comments = CommentSerializer(many=True, read_only=True, source='comments.all')
    date = serializers.SerializerMethodField() 

    class Meta:
        model = Blog
        fields = ['id', 'user', 'nickname', 'title', 'body', 'date', 'comments']

    def get_date(self, obj):
        return obj.date.strftime("%Y-%m-%d")  