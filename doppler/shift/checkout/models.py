"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Checkout
Part: Models implementation
"""
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from doppler.shift.catalog.models import Product
from ..catalog.models import MULTIPLE_PRICES
if MULTIPLE_PRICES:
    from ..catalog.models import Price
import random

class Cart(object):
    """
    Shopping cart. Session-based, available both for authorized and unauthorized users.
    """
    CART_ID_SESSION_KEY = 'cart_id' #TODO: move to settings configuration file
    CART_ID_CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    CART_ID_LENGTH = 50

    def __init__(self, request):
        self.key = Cart._get_session_stored_cart_id(request)

    @classmethod
    def _generate_cart_id(cls):
        """
        Private method for unique cart id generation
        """
        cart_id = ''
        rand_border = len(cls.CART_ID_CHARACTERS) - 1
        for y in range(cls.CART_ID_LENGTH):
            cart_id += cls.CART_ID_CHARACTERS[random.randint(0, rand_border)]
        return cart_id

    @classmethod
    def _get_session_stored_cart_id(cls, request):
        """
        Retrieve session-stored cart-id
        """
        if not request.session.get(cls.CART_ID_SESSION_KEY, False):
            request.session[cls.CART_ID_SESSION_KEY] = cls._generate_cart_id()
        return request.session[cls.CART_ID_SESSION_KEY]

    @property
    def items(self):
        """
        Get cart items for current cart basing on key
        """
        return CartItem.objects.filter(key=self.key)

    @property
    def is_empty(self):
        """
        True if cart is empty
        """
        return not CartItem.objects.filter(key=self.key).count()

    def clear(self):
        """
        Clear the cart instance
        """
        self.items.delete()

    @property
    def total_price(self):
        """
        Cart total price
        """
        return reduce(lambda res, x: res + x, [item.total_price for item in self.items.all()])

    @property
    def total_quantity(self):
        """
        Get cart total quantity
        """
        return reduce(lambda res, x: res + x, [item.quantity for item in self.items.all()])

    @property
    def distinct_quantity(self):
        """
        Get total distinct quantity
        """
        return self.items.count()

    def update_quantities(self, dict):
        """
        Updates item quantities basing on provided dictionary [cart_item_id: product_quantity]
        """
        for id in dict:
            self.items.get(pk=id).update_quantity(dict[id])

class CartItem(models.Model):
    """
    Shopping cart item.
    """
    class Meta:
        verbose_name = _('cart item')
        verbose_name_plural = _('cart items')
        ordering = ['created']
        unique_together = [('cart_key', 'shipment')]

    cart_key = models.CharField(max_length=50, verbose_name=_('cart key'))
    shipment = models.ForeignKey(to=Price, verbose_name=_('shipment'))
    quantity = models.IntegerField(default = 1, verbose_name = _('quantity'))
    created = models.DateTimeField(auto_now_add = True, verbose_name = _('created'))
    modified = models.DateTimeField(auto_now = True, verbose_name = _('modified'))

    @property
    def total_price(self):
        """
        Return total price as product price times product quantity
        """
        return self.quantity * self.shipment.price

    def augment_quantity(self, quantity):
        """
        Augments product quantity by provided value
        """
        self.quantity += int(quantity)
        self.save()

    def update_quantity(self, quantity):
        """
        Updates product quantity with provided value
        """
        self.quantity = int(quantity)
        self.save()