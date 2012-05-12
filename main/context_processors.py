from django.conf import settings

def login_url(request):
    return {
        'LOGIN_URL': settings.LOGIN_URL,
        'request': request
        }

def default_avatar_url(request):
    return {
        'DEFAULT_AVATAR_URL': settings.DEFAULT_AVATAR_URL,
        'request': request
    }