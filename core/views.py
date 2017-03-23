from django.shortcuts import render
from django.views.generic import TemplateView
from blogs.models import Blog, Post

class HomePageView(TemplateView):

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['blog_count'] = Blog.objects.all().count()
        context['post_count'] = Post.objects.all().count()
        return context