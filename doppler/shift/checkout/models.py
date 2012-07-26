"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Checkout
Part: Models implementation
"""
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from model_utils import Choices
from session_cart.cart import CartItem, Cart
from doppler.shift.catalog.models import Product, MULTIPLE_PRICES
from .signals import order_created, order_state_changed
if MULTIPLE_PRICES:
    from doppler.shift.catalog.models import Price

CartItem.total_price = lambda self: self.item.value * self.quantity
Cart.total_price = lambda self: reduce(lambda res, x: res + x, [item.total_price() for item in self])

from django.db import models

class Order(models.Model):
    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ['modified',]

    user = models.ForeignKey(to=User, verbose_name=_('user'), related_name='orders')
    created = models.DateTimeField(auto_now_add = True, verbose_name = _('created'))
    modified = models.DateTimeField(auto_now = True, verbose_name = _('modified'))

    STATUS = Choices(
        ('new', _('new')),
        ('processing', _('processing')),
        ('awaits shipping', _('awaits shipping')),
        ('shipped', _('shipped')),
        ('cancelled', _('cancelled')),
    )
    status = models.CharField(choices=STATUS, default=STATUS.new, max_length=30)

    customer_name = models.CharField(max_length=30, blank=False, null=False, verbose_name=_('customer name'))
    customer_phone = models.CharField(max_length=20, default='', blank=False, null=False, verbose_name=_('customer phone'))
    customer_email = models.EmailField(blank=False, null=False, verbose_name=_('customer e-mail'))
    delivery_address = models.TextField(default='', blank=False, null=False, verbose_name=_('delivery address'))
    comment = models.TextField(blank=True, default='', verbose_name=_('comment'))
    ip_address = models.IPAddressField(verbose_name=_('IP adress'))

    def __unicode__(self):
        return _('Order #%d') % self.id

    @property
    def total_price(self):
        return reduce(lambda res, x: res+x, [item.total_price for item in self.items.all()])

    @property
    def total_quantity(self):
        return reduce(lambda res, x: res+x, [item.quantity for item in self.items.all()])

    @models.permalink
    def get_absolute_url(self):
        return 'doppler_shift_order', (), {'order_id': self.pk}

    #TODO: save method override for remainder updates basing on status change; and also status change notifications
    def save(self, *args, **kwargs):
        if not self.id:
            super(Order, self).save(*args, **kwargs)
            order_created.send(sender=self, order=self)
        else:
            try:
                existed_order = Order.objects.get(id=self.id)
                existed_order_status = existed_order.status
                if existed_order_status != self.status:
                    super(Order, self).save(*args, **kwargs)
                    order_state_changed.send(sender=self, order=self)
            except Order.DoesNotExist:
                super(Order, self).save(*args, **kwargs)
                order_created.send(sender=self, order=self)

class OrderItem(models.Model):
    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')
        ordering = ['order', 'modified',]

    order = models.ForeignKey(to=Order, verbose_name=_('order'), related_name='items')
    product = models.ForeignKey(to=Product, verbose_name=_('product'), related_name='orders')
    if MULTIPLE_PRICES:
        shipment = models.ForeignKey(to=Price, verbose_name=_('shipment'), related_name='orders', null=True, blank=True)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    price = models.PositiveIntegerField(verbose_name=_('price'))
    created = models.DateTimeField(auto_now_add = True, verbose_name = _('created'))
    modified = models.DateTimeField(auto_now = True, verbose_name = _('modified'))

    @property
    def total_price(self):
        return self.price * self.quantity

    def save(self, **kwargs):
        super(OrderItem, self).save(**kwargs)
        self.order.save() # updating parent order entity modified timestamp