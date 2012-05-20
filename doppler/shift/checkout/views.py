"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Views
"""
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils.translation import ugettext_lazy as _
from .models import Cart

def cart(request, template_name='doppler/shift/checkout/cart.haml'):
    """
    Cart view
    """
    cart = Cart.get_cart(request=request)
    return render_to_response(template_name, {'cart': cart}, context_instance=RequestContext(request))