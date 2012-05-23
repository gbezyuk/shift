"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Checkout
Part: Models implementation
"""
from django import forms
from django.utils.translation import ugettext_lazy as _
from querystring_parser import parser
from .models import Order, OrderItem
from doppler.shift.catalog.models import ProductNotAvailableError

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

    success_message = _('cart was successfully updated')

class OrderForm(forms.ModelForm):
    """
    Order form
    """
    class Meta:
        model = Order
        exclude = ['user', 'ip_address', 'status']

    def __init__(self, request, **kwargs):
        super(OrderForm, self).__init__(**kwargs)
        self.request = request
        self.fields['customer_name'].initial = self.request.user.profile.first_name
        self.fields['customer_email'].initial = self.request.user.email
        self.fields['customer_phone'].initial = self.request.user.profile.phone
        self.fields['delivery_address'].initial = _('enter your delivery address here')
        self.fields['comment'].initial = _('enter your custom comment here')

    def is_valid(self):
        if not super(OrderForm, self).is_valid():
            return False
        for cart_position in self.request.cart:
            if cart_position.quantity > cart_position.item.remainder:
                raise ProductNotAvailableError(
                    message='Product is not available: %s, %d; only %d available'
                        % (cart_position.item.product, cart_position.quantity, cart_position.item.remainder),
                    product = cart_position.item.product,
                    shipment=cart_position.item,
                    maximal_available_quantity=cart_position.item.remainder,
                    requested_quantity=cart_position.quantity)
        return True

    def save(self, commit=True):
        order = super(OrderForm, self).save(commit=False)
        order.user = self.request.user
        order.ip_address = self.request.META['REMOTE_ADDR']
        if commit:
            order.save()
            for cart_position in self.request.cart:
                cart_position.item.decrease_remainer(cart_position.quantity)
                OrderItem(order=order,
                    product=cart_position.item.product,
                    quantity=cart_position.quantity,
                    price=cart_position.item.value,
                ).save()
            self.request.cart.empty()
        return order

    cart_is_empty_message = _('Your cart is empty. You can not make an empty order, so please fill your cart first.')
    success_message = _('Your order is successfully made!')