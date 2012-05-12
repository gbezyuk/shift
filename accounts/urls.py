from django.conf.urls.defaults import patterns, include, url
from .views import profile, edit_profile, change_avatar, users

urlpatterns = patterns('',
    url(r'auth/', include('accounts.auth.urls')),
    url(r'profile/$', profile, name='profile'),
    url(r'profile/edit/$', edit_profile, name='edit_profile'),
    url(r'profile/change_avatar/$', change_avatar, name='change_avatar'),
    url(r'users/$', users, name='users'),
)