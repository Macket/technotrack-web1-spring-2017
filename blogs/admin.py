from django.contrib import admin
from .models import Blog, Post, Category, Like

admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Like)