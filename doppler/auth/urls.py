"""
Studio: Doppler
Module: Basic user authorization
Part: Urls
"""
from django.conf.urls.defaults import patterns, include, url
from .views import login, logout

urlpatterns = patterns('',
    url(r'^login/$', login, name='doppler_auth_login'),
    url(r'^logout/$', logout, name='doppler_auth_logout'),
)
