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
        self.cart = Cart.get_cart(request)
        self.post_dict = parser.parse(request.POST.urlencode())
        for item in Cart.get_items(request):
            field_name = 'item_count[%d]' % (item.id,)
            self.fields[field_name] = forms.IntegerField(min_value=1, initial=item.quantity, max_value=9999999)
            field_name = 'remove_item[%d]' % (item.id,)
            self.fields[field_name] = forms.BooleanField(required=False)

    def update_count(self):
        """
        Cart update count form action
        """
        self.cart.update_quantities(self.post_dict['item_count'])

    def remove_selected(self):
        """
        Cart remove selected form action
        """
        self.cart.remove_items(list(self.post_dict['remove_item']))

    def is_valid(self):
        """
        Validation check
        """
        return self.cart and self.post_dict and 'item_count' in self.post_dict