# coding: utf-8
from __future__ import unicode_literals
from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'


class Blog(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author_blog', default=1)
    category = models.ManyToManyField(Category, related_name='category_blog')

    class Meta:
        verbose_name = u'Блог'
        verbose_name_plural = u'Блоги'
        ordering = ('-updated_at',)


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    blog = models.ForeignKey(Blog, related_name='post')
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author_post', default=1)

    class Meta:
        verbose_name = u'Пост'
        verbose_name_plural = u'Посты'
        ordering = ('-updated_at',)

