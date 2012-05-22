"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Views
"""
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from .forms import UpdateCartForm
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse

def clear_cart(request):
    request.cart.empty()
    return redirect_to(request, reverse('doppler_shift_cart'), permanent=False)

def cart(request, template_name='doppler/shift/checkout/cart.haml'):
    """
    Cart view
    """
    form = UpdateCartForm(request, data=request.POST or None)
    if form.is_valid():
        form.update_cart()
        messages.success(request, UpdateCartForm.success_message)
    return render_to_response(template_name, {'form': form }, context_instance=RequestContext(request))