"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Checkout
Part: Models implementation
"""
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Cart

class AddProductToCartForm(forms.Form):
    """
    To be used with product model
    """
    quantity = forms.IntegerField(initial=1, min_value=1, max_value=9999999, label=_("quantity"))

    def __init__(self, product, **kwargs):
        """
        Overloaded constructor
        """
        super(AddProductToCartForm, self).__init__(**kwargs)
        self.product = product

    def clean_quantity(self):
        """
        Quantity custom validation
        """
        if self.cleaned_data['quantity'] > self.product.remainder:
            raise forms.ValidationError(_('%d is maximum quantity we can offer for this product') % self.product.remainder)
        return self.cleaned_data['quantity']

    def save(self, request):
        """
        Creates or updates a CartItem model instance
        """
        cart = Cart.get_cart(request=request, create_if_not_exist=True)
        cart.insert_item(self.product, self.cleaned_data['quantity'])

    success_message = _('product was successfully added to your cart')