from .views import category_fallback, product_fallback
from django.http import Http404
from django.conf import settings

class CategoryFallbackMiddleware(object):
    """
    This middleware hooks over 404 and checking existing enabled categories.
    Based on original django.contrib.flatpages.middleware.FlatpageFallbackMiddleware
    """
    def process_response(self, request, response):
        if response.status_code != 404:
            return response
        try:
            return category_fallback(request, request.path_info)
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response

class ProductFallbackMiddleware(object):
    """
    This middleware hooks over 404 and checking existing enabled categories.
    Based on original django.contrib.flatpages.middleware.FlatpageFallbackMiddleware
    """
    def process_response(self, request, response):
        if response.status_code != 404:
            return response
        try:
            return product_fallback(request, request.path_info)
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response


