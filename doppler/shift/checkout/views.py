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
from doppler.shift.catalog.models import ProductNotAvailableError
from .forms import UpdateCartForm, OrderForm
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

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
@transaction.commit_on_success
def make_order(request, template_name='doppler/shift/checkout/make_order.haml'):
    """
    Order form view
    """
    if not request.cart:
        messages.success(request, OrderForm.cart_is_empty_message)
        return redirect_to(request, reverse('doppler_shift_cart'), permanent=False)
    form = OrderForm(data=request.POST or None, request=request)
    try:
        if form.is_valid():
            form.save()
            messages.success(request, OrderForm.success_message)
            return redirect_to(request, reverse('doppler_shift_cart'), permanent=False)
    except ProductNotAvailableError, e:
        messages.error(request, _('Execuse us, %d is too much for %s, only %d available')
            % (e.requested_quantity, e.product, e.maximal_available_quantity))
    return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))