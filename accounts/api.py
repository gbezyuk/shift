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

class ProfileResource(ModelResource):
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'profile'
        include_resource_uri = False
        include_absolute_url = False
        excludes = ['created', 'modified', 'avatar', 'id']

class UserResource(ModelResource):
    profile = fields.ToOneField(ProfileResource, 'get_profile', full=True)

    class Meta:
        resource_name = 'user'
        queryset = User.objects.all()
        excludes = ['email', 'password', 'is_staff', 'is_active', 'is_superuser', 'date_joined', 'first_name', 'last_name', 'last_login']