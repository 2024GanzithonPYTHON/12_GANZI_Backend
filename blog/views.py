from .models import Blog
from .serializers import BlogSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

"""
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def blog_list(request):
	if request.method == 'GET':
		blogs = Blog.objects.all()
		serializer = BlogSerializer(blogs, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
	elif request.method == 'POST':
		serializer = BlogSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
	return Response(status=status.HTTP_400_BAD_REQUEST)

'''
한 블로그 조회
'''
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsOwnerOrReadOnly])
def blog_detail(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
        if request.method == 'GET':
            serializer = BlogSerializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = BlogSerializer(blog, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            blog.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
"""
class BlogList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BlogDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    def get_object(self, pk):
        blog = get_object_or_404(Blog, pk=pk)
        return blog

    def get(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog = self.get_object(pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)