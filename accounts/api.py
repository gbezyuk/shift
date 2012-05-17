"""
Studio: Doppler
Author: Grigoriy Beziuk
Project: Django Application Skeleton
Module: User accounts
Part: Tastypie API
"""
from tastypie.resources import ModelResource
from .models import UserProfile
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization

class ProfileResource(ModelResource):
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'profile'
        include_resource_uri = False
        include_absolute_url = False
        excludes = ['created', 'modified', 'avatar', 'id']
        allowed_methods = ['get']

class UserResource(ModelResource):
    """
    WARNING!
    If you`re using Apache & mod_wsgi, you will need to enable WSGIPassAuthorization On.
    See this post for details: http://www.nerdydork.com/basic-authentication-on-mod_wsgi.html
    """
    profile = fields.ToOneField(ProfileResource, 'get_profile', full=True)

    class Meta:
        resource_name = 'user'
        queryset = User.objects.all()
        excludes = ['email', 'password', 'is_staff', 'is_active', 'is_superuser', 'date_joined', 'first_name', 'last_name', 'last_login']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get']