# ganzithon/blog/models.py
from django.db import models
from accounts.models import CustomUser

class Blog(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
