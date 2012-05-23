"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Views
"""
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from .forms import UpdateCartForm, OrderForm
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

def clear_cart(request):
    """
    Clear cart and redirect back to basic cart view
    """
    request.cart.empty()
    return redirect_to(request, reverse('doppler_shift_cart'), permanent=False)

def cart(request, template_name='doppler/shift/checkout/cart.haml'):
    """
    Basic cart view
    """
    form = UpdateCartForm(request, data=request.POST or None)
    if form.is_valid():
        form.update_cart()
        messages.success(request, UpdateCartForm.success_message)
    return render_to_response(template_name, {'form': form }, context_instance=RequestContext(request))

@login_required
#@transaction.commit_on_success
def make_order(request, template_name='doppler/shift/checkout/make_order.haml'):
    """
    Order form view
    """
    form = OrderForm(data=request.POST or None, request=request)
    if form.is_valid():
        form.save()
    return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))