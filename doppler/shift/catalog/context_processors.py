from .models import Category

def categories(request):
    return {
        'categories': Category.objects.filter(enabled=True, parent=None),
        'request': request
    }