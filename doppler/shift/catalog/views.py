"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Views implementation
"""
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.conf import settings
from django.core.xheaders import populate_xheaders
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.template.context import RequestContext
from django.utils.translation import ugettext_lazy as _
from .models import Category, Product
from ..checkout.forms import AddProductToCartForm


def index(request, template_name='doppler/shift/catalog/index.haml'):
    """
    Catalog index page view. Contains root categories.
    """
    return render_to_response(
        template_name,
        {'root_categories': Category.enabled_root.all()},
        context_instance=RequestContext(request)
    )


def product_fallback(request, url):
    if not url.startswith('/'):
        url = '/' + url
    if not url.endswith('/'):
        url += '/'
    slug = url[1:][:-1]
    try:
        product = get_object_or_404(Product, slug__exact=slug, enabled=True)
    except Http404:
        raise
    if product.is_inside_disabled_parent:
        raise Http404
    return render_product(request, product)


def category_fallback(request, url):
    if not url.startswith('/'):
        url = '/' + url
    if not url.endswith('/'):
        url += '/'
    slug = url[1:][:-1]
    try:
        category = get_object_or_404(Category, slug__exact=slug, enabled=True)
    except Http404:
        raise
    if category.is_inside_disabled_parent:
        raise Http404
    return render_category(request, category)


@csrf_protect
def render_category(request, category, template_name='doppler/shift/catalog/category.haml'):
    products = category.enabled_products
    subcategories = category.children.filter(enabled=True)
    for product in products:
        product.form = AddProductToCartForm( product = product )
    return render_to_response(
        template_name,
        {
        'category': category,
        'products': products,
        'subcategories': subcategories,
        },
        context_instance=RequestContext(request)
    )


@csrf_protect
def render_product(request, product, template_name='doppler/shift/catalog/product.haml'):
    """
    Catalog product details page view. Contains product details
    """
    category = product.category
    form = AddProductToCartForm( data = request.POST or None, product = product )
    if form.is_valid():
        form.save(request)
        if not request.is_ajax():
            messages.success(request, AddProductToCartForm.success_message)
    if request.is_ajax():
        from django.http import HttpResponse
        from django.utils import simplejson
        cart = getattr(request, 'cart', None)
        data = {
            'result': True,
            'in_cart': cart.items_total,
        }
        return HttpResponse(
            simplejson.dumps(data, sort_keys=True, indent=4),
            mimetype='application/json'
        )

    return render_to_response(
        template_name,
        {
        'category': category,
        'product': product,
        'form': form,
        },
        context_instance=RequestContext(request)
    )