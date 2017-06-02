# coding: utf-8

from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
)
from django.contrib.auth.views import _get_login_redirect_url
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic import TemplateView, CreateView

from blogs.models import Blog, Post
from .models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm



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
        return HttpResponse('OK')


def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          extra_context=None, redirect_authenticated_user=False):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, ''))

    if redirect_authenticated_user and request.user.is_authenticated:
        redirect_to = _get_login_redirect_url(request, redirect_to)
        if redirect_to == request.path:
            raise ValueError(
                "Redirection loop for authenticated user detected. Check that "
                "your LOGIN_REDIRECT_URL doesn't point to a login page."
            )
        return HttpResponseRedirect(redirect_to)
    elif request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponse('OK')
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)