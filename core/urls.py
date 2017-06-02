from .views import *
from django.conf.urls import url
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name="home_page"),
    url(r'^login$', login, {'template_name': 'core/login.html'}, name="login"),
    url(r'^logout$', logout, name="logout"),
    url(r'^registration$', RegisterFormView.as_view(), name="registration"),
]