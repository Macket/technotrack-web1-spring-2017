# coding: utf-8
from django import forms
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View

from comments.models import Comment
from .models import Blog, Post, Category, Like
import logging

logger = logging.getLogger(__name__)


class SortForm(forms.Form):

    sort = forms.ChoiceField(
        choices=(
            ('title', u'Заголовок'),
            ('description', u'Описание'),
        ),
        widget=forms.RadioSelect
    )
    search = forms.CharField(required=False, widget=forms.TextInput)


class UpdateBlog(UpdateView):

    template_name = "blogs/editblog.html"
    model = Blog
    fields = ('title', 'description')

    def get_success_url(self):
        return resolve_url('blogs:blog_view', pk=self.object.pk)

    def get_queryset(self):
        return super(UpdateBlog, self).get_queryset().filter(author = self.request.user)

    def form_valid(self, form):
        response = super(UpdateBlog, self).form_valid(form)
        return HttpResponse('OK')


class CreateBlog(CreateView):

    template_name = "blogs/addblog.html"
    model = Blog
    fields = ('title', 'description', 'category')

    def get_success_url(self):
        return resolve_url('blogs:blog_view', pk=self.object.pk)

    def get_form(self, form_class=None):
        form = super(CreateBlog, self).get_form()
        form.fields['category'].queryset = Category.objects.all()
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateBlog,self).form_valid(form)


class BlogList(ListView):
    template_name = "blogs/blog_list.html"
    queryset = Blog.objects.all()
    sortform = None

    def dispatch(self, request, *args, **kwargs):
        self.sortform = SortForm(self.request.GET)
        return super(BlogList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context['sortform'] = self.sortform
        return context

    def get_queryset(self):
        qs = super(BlogList, self).get_queryset()
        qs = qs.annotate_everything()
        if self.sortform.is_valid():
            qs = qs.order_by(self.sortform.cleaned_data['sort'])
            if self.sortform.cleaned_data['search']:
                qs = qs.filter(title__icontains=self.sortform.cleaned_data['search'])
        return qs


class BlogView(DetailView):
    template_name = "blogs/blog.html"
    queryset = Blog.objects.all()

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(blog=self.object).select_related('author', 'blog', 'blog__author')
        return context


class CreatePost(CreateView):

    template_name = "blogs/addpost.html"
    model = Post
    fields = ('title', 'text', 'blog')

    def get_success_url(self):
        return resolve_url('blogs:post_view', pk=self.object.pk)

    def get_form(self, form_class=None):
        form = super(CreatePost,self).get_form()
        form.fields["blog"].queryset = Blog.objects.all().filter(author=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        logger.info("New post created")
        return super(CreatePost,self).form_valid(form)


class PostDetail(CreateView):
    model = Comment
    template_name = 'blogs/post_view.html'
    fields = ('text',)

    def get_success_url(self):
        return resolve_url('blogs:post_view', pk=self.postobject.id)

    def form_valid(self, form):
        form.instance.post = self.postobject
        form.instance.author = self.request.user
        return super(PostDetail, self).form_valid(form)

    def dispatch(self, request, pk=None, *args, **kwargs):
        self.postobject = get_object_or_404(Post, id=pk)
        return super(PostDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['post'] = self.postobject
        return context


class UpdatePost(UpdateView):
    template_name = "blogs/editpost.html"
    model = Post
    fields = ('title', 'text')

    def get_success_url(self):
        return resolve_url('blogs:blog_view', pk=self.object.blog.id)

    def get_queryset(self):
        return super(UpdatePost, self).get_queryset().filter(author=self.request.user)

    def form_valid(self, form):
        response = super(UpdatePost, self).form_valid(form)
        return HttpResponse('OK')


class CommentSourceView(DetailView):
    queryset = Post.objects.all()
    template_name = "blogs/commentsource.html"


class LikeView(View):

    def dispatch(self, request, pk=None, *args, **kwargs):
        self.postobject = get_object_or_404(Post, id=pk)
        return super(LikeView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.postobject.likes.filter(author=self.request.user).exists():
            like = Like()
            like.post = self.postobject
            like.author = self.request.user
            like.save()
        else:
            self.postobject.likes.filter(author=self.request.user).delete()
        return HttpResponse(self.postobject.likes.count())

    def get(self, request):
        return HttpResponse(self.postobject.likes.count())
