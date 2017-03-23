from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Blog, Post

class BlogList(ListView):
    template_name = "blogs/blog_list.html"
    queryset = Blog.objects.all()

class BlogView(DetailView):
    template_name = "blogs/blog.html"
    queryset = Blog.objects.all()

# class PostList(ListView):
#     template_name = "blogs/post_view.html"
#     queryset = Post.objects.all()

class PostView(DetailView):
    template_name = "blogs/post_view.html"
    queryset = Post.objects.all()