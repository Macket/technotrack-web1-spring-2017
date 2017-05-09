from .views import *
from django.conf.urls import url
from django.contrib.auth.decorators import  login_required

urlpatterns = [
    url(r'^$', BlogList.as_view(), name='blog_list'),
    url(r'^(?P<pk>\d+)$', BlogView.as_view(), name="blog_view"),
    url(r'^(?P<pk>\d+)/edit/$', UpdateBlog.as_view(), name="editblog"),
    url(r'^post/(?P<pk>\d+)$', login_required(PostDetail.as_view()), name="post_view"),
    url(r'^post/(?P<pk>\d+)/commentsource/$', login_required(CommentSourceView.as_view()), name="commentsource"),
    url(r'^new/$', login_required(CreateBlog.as_view()), name="createblog"),
    url(r'^post/new/$', login_required(CreatePost.as_view()), name="createpost"),
    url(r'^post/(?P<pk>\d+)/edit/$', login_required(UpdatePost.as_view()), name="editpost"),
    url(r'^post/(?P<pk>\d+)/likes/$', login_required(LikeView.as_view()), name="post_likes"),
]