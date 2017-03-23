from .views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name="home_page"),
]