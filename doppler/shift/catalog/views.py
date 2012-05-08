"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Views implementation
"""
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from .models import Category

def index(request, template_name='doppler/shift/catalog/index.haml'):
    """
    Catalog index page view. Contains root categories.
    """
    return render_to_response(
        template_name,
        {'root_categories': Category.enabled_root.all()},
        context_instance=RequestContext(request))

def category(request, category_id, template_name='doppler/shift/catalog/category.haml'):
    """
    Catalog category details page view. Contains category details and its subcategories and products.
    """
    category = get_object_or_404(Category, pk=category_id, enabled=True)
    products = category.enabled_products
    subcategories = category.children.filter(enabled=True)
    return render_to_response(
        template_name,
        {
            'category': category,
            'products': products,
            'subcategories': subcategories,
        },
        context_instance=RequestContext(request))
