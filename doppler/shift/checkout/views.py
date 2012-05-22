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
    return render_to_response(template_name, {'form': form }, context_instance=RequestContext(request))

#def show(request, template_name="cart/cart.html"):
#    form = UpdateCartForm(request, request.POST or cart.get_cart_form_dictionary(request))
#    if request.POST:
#        if form.is_valid():
#            action = request.POST['action']
#            post_dict = parser.parse(request.POST.urlencode())
#            if action == 'remove_selected':
#                cart.remove_items_from_cart(request, list(post_dict['remove_item']))
#            if action == 'recalculate':
#                cart.update_products_count(request, post_dict['item_count'])
#            if action == 'checkout':
#                return redirect('cart:checkout')
#    if not form.is_valid():
#        form = UpdateCartForm(request, cart.get_cart_form_dictionary(request))
#    cart_item_count = cart.cart_distinct_item_count(request)
#    cart_items = cart.get_cart_items(request)
#    cart_total = cart.get_cart_total(request)
#    cart_total_count = cart.get_cart_total_count(request)
#    cart_total_discounted = cart.get_cart_total_discounted(request)
#    cart_discount_size = cart.get_discount_size(request)
#    cart_discount_text = cart.get_discount_text(request)
#
#    return render_to_response(template_name, locals(),
#        context_instance=RequestContext(request))