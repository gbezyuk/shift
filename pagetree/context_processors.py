from .models import Page

def root_pages(request):
    return {
        'root_pages': Page.objects.filter(is_enabled=True, parent=None),
        'request': request
        }