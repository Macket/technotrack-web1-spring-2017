from .views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^$', BlogList.as_view(), name='blog_list'),
    url(r'^(?P<pk>\d+)$', BlogView.as_view(), name="blog_view"),
    url(r'^post/(?P<pk>\d+)$', PostView.as_view(), name="post_view"),
]