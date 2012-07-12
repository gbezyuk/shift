from .views import page
from django.http import Http404
from django.conf import settings

class PageFallbackMiddleware(object):
    """
    This middleware hooks over 404 and checking existing enabled pages.
    Based on original django.contrib.flatpages.middleware.FlatpageFallbackMiddleware
    """
    def process_response(self, request, response):
        if response.status_code != 404:
            return response
        try:
            return page(request, request.path_info)
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response