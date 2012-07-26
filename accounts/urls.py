"""
Studio: Doppler
Author: Grigoriy Beziuk
Project: Django Application Skeleton
Module: User accounts
Part: Urls
"""
from django.conf.urls.defaults import patterns, include, url
from .views import profile, edit_profile, change_avatar#, users, user
from .api import UserResource
entry_resource = UserResource()

urlpatterns = patterns('',
    url(r'auth/', include('accounts.auth.urls')),
    url(r'profile/$', profile, name='profile'),
    url(r'profile/edit/$', edit_profile, name='edit_profile'),
    url(r'profile/change_avatar/$', change_avatar, name='change_avatar'),
#    url(r'^api/', include(entry_resource.urls)),
#    uncomment lines bellow to enable user list and user details views
#    url(r'users/$', users, name='users'),
#    url(r'users/(?P<user_id>\d+)/$', user, name='user'),

)
