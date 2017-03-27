# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from blogs.models import Post
from django.conf import settings


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    text = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments')

    class Meta:
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'
        ordering = ('-updated_at',)