"""
Studio: Doppler
Module: Basic user authorization
Part: Urls
"""
from django.conf.urls.defaults import patterns, include, url
from .views import login, logout

urlpatterns = patterns('',
    url(r'^login/$', login, name='auth_login'),
    url(r'^logout/$', logout, name='auth_logout'),
)
