# ganzithon/blog/admin.py
from django.contrib import admin
from .models import Blog

class BlogAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(Blog, BlogAdmin)