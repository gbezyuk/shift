from .models import Category

def categories(request):
    return {
        'categories': Category.tree.filter(enabled=True),
        'request': request
    }