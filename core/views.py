# coding: utf-8
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from blogs.models import Blog, Post
from .models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField


class HomePageView(TemplateView):

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['blog_count'] = Blog.objects.all().count()
        context['post_count'] = Post.objects.all().count()
        return context


class UserRegForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "avatar")
        field_classes = {'username': UsernameField}


class RegisterFormView(CreateView):
    form_class = UserRegForm
    success_url = "/"
    template_name = "core/registration.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)