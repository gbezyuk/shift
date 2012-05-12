"""
Studio: Doppler
Author: Grigoriy Beziuk
Project: Django Application Skeleton
Module: Basic user authorization
Part: Views
"""
from django.utils.translation import ugettext_lazy as _
from django.views.generic.simple import direct_to_template, redirect_to
from .forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

def login(request, template_name='accounts/auth/login.haml'):
    """
    Login view. Redirects to url specified in 'next' GET/POST parameter after successful login
    """
    form = LoginForm(data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                messages.success(request, _('You have successfully logged in'))
                if 'next' in request.GET and request.GET['next']:
                    return redirect_to(request, request.GET['next'], permanent=False)
                elif 'next' in request.POST and request.POST['next']:
                    return redirect_to(request, request.POST['next'], permanent=False)
                else:
                    return redirect_to(request, '/', permanent=False)
            else:
                messages.error(request, _('This account is disabled'))
        else:
            messages.error(request, _('Invalid login/password pair'))
    return direct_to_template(request, template_name, locals())

def logout(request):
    """
    Logout view. Redirects to url specified in 'next' POST/GET param after logout
    """
    auth_logout(request)
    if 'next' in request.GET and request.GET['next']:
        return redirect_to(request, request.GET['next'], permanent=False)
    elif 'next' in request.POST and request.POST['next']:
        return redirect_to(request, request.POST['next'], permanent=False)
    else:
        return redirect_to(request, '/', permanent=False)
