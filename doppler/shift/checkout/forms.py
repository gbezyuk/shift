"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Checkout
Part: Models implementation
"""
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Cart
from querystring_parser import parser

class AddProductToCartForm(forms.Form):
    """To be used with product model"""
    quantity = forms.IntegerField(initial=1, min_value=1, label=_("quantity"))

    def __init__(self, shipment, **kwargs):
        """Overloaded constructor"""
        super(AddProductToCartForm, self).__init__(**kwargs)
        self.shipment = shipment

    def is_valid(self):
        """Buying nothing is always invalid =)"""
        if not self.shipment:
            return False
        return super(AddProductToCartForm, self).is_valid()

    def clean_quantity(self):
        """No more than shop can offer can be added to cart"""
        if self.cleaned_data['quantity'] > self.shipment.remainder:
            raise forms.ValidationError(_('%d is maximum quantity we can offer for this product') % self.shipment.remainder)
        return self.cleaned_data['quantity']

    def save(self, request):
        """put shipment to cart using session_cart interface"""
        request.cart.append(self.shipment, self.cleaned_data['quantity'])

    success_message = _('product was successfully added to your cart')

class UpdateCartForm(forms.Form):
    """
    Cart update form
    """
    def __init__(self, request, *args, **kwargs):
        """
        Fields are being created dynamically basing on current user/request cart instance
        """
        super(UpdateCartForm, self).__init__(*args, **kwargs)
        self.request = request
        for item in request.cart:
            field_name = 'item_quantity[%d]' % (item.item.id,)
            self.fields[field_name] = forms.IntegerField(min_value=1, initial=item.quantity)
            field_name = 'remove_item[%d]' % (item.item.id,)
            self.fields[field_name] = forms.BooleanField(required=False)

    def update_cart(self):
        """
        Cart update form action: update quantities, remove marked for removal items
        """
        post_dict = parser.parse(self.request.POST.urlencode())
        self.request.cart.update_quantities(post_dict['item_quantity'])
        if 'remove_item' in post_dict:
            self.request.cart.remove_items(list(post_dict['remove_item']))
