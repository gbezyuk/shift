"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Checkout
Part: Models implementation
"""
from django.utils.translation import ugettext_lazy as _
from django.db import models
from doppler.shift.catalog.models import Product
import random

class Cart(models.Model):
    """
    Shopping cart. Session-based, available both for authorized and unauthorized users.
    """
    created = models.DateTimeField(auto_now_add = True, verbose_name = _('created'))
    modified = models.DateTimeField(auto_now = True, verbose_name = _('modified'))
    key = models.CharField(max_length = 50, verbose_name = _('session key'))

    CART_ID_SESSION_KEY = 'cart_id' #TODO: move to settings configuration file
    CART_ID_CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'

    @classmethod
    def _generate_cart_id(cls):
        cart_id = ''
        characters = cls.CART_ID_CHARACTERS
        cart_id_length = 50
        for y in range(cart_id_length):
            cart_id += characters[random.randint(0, len(characters)-1)]
        try:
            Cart.objects.get(key=cart_id)
            cart_id = cls._generate_cart_id()
        except Cart.DoesNotExist:
            return cart_id

    @classmethod
    def get_session_stored_cart_id(cls, request):
        if not request.session.get(cls.CART_ID_SESSION_KEY, False):
            request.session[cls.CART_ID_SESSION_KEY] = cls._generate_cart_id()
        return request.session[cls.CART_ID_SESSION_KEY]

    @classmethod
    def get_cart(cls, request):
        key = cls.get_session_stored_cart_id(request)
        try:
            return Cart.objects.get(key=key)
        except Cart.DoesNotExist:
            return None

    @classmethod
    def get_cart_items(cls, request):
        cart = cls.get_cart(request)
        if cart:
            return cart.cart_items.all()
        else:
            return []

class CartItem(models.Model):
    """
    Shopping cart item.
    """
    class Meta:
        verbose_name = _('cart item')
        verbose_name_plural = _('cart items')
        ordering = ['created']

    cart = models.ForeignKey(to=Cart, verbose_name=_('cart'), related_name='cart_items')
    product = models.ForeignKey(to=Product, verbose_name=_('product'))
    price = models.DecimalField(verbose_name=_('price'), max_digits=10, decimal_places=3)
    quantity = models.IntegerField(default = 1, verbose_name = _('quantity'))
    created = models.DateTimeField(auto_now_add = True, verbose_name = _('created'))
    modified = models.DateTimeField(auto_now = True, verbose_name = _('modified'))

    @property
    def total_price(self):
        """
        Return total price as product price times product quantity
        """
        return self.quantity * self.price

    def augment_quantity(self, quantity):
        """
        Augments product quantity by provided value
        """
        self.quantity += int(quantity)
        self.save()