"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Models implementation
"""
from django.db import models
from django.db.models.aggregates import Min
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel
from .managers import EnabledTreeManager, EnabledRootManager
from django.conf import settings

try:
    MULTIPLE_CATEGORIES = settings.DOPPLER_SHIFT_CATALOG_PRODUCT_MULTIPLE_CATEGORIES
except AttributeError:
    MULTIPLE_CATEGORIES = False
try:
    MULTIPLE_PRICES = settings.DOPPLER_SHIFT_CATALOG_PRODUCT_MULTIPLE_PRICES
except AttributeError:
    MULTIPLE_PRICES = False

class Category(MPTTModel):
    """
    Basic catalog entity - a category
    """
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['tree_id', 'lft'] # feincms TreeEditor needs this ordering definition

    name = models.CharField(max_length=255, verbose_name=_('name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    enabled = models.BooleanField(default=True, verbose_name=_('enabled'))
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_('parent'))
    created = models.DateTimeField(auto_now_add = True, verbose_name = _('created'))
    modified = models.DateTimeField(auto_now = True, verbose_name = _('modified'))

    enabled_tree = EnabledTreeManager()
    enabled_root = EnabledRootManager()

    def __unicode__(self):
        return self.name

class Product(models.Model):
    """
    Basic catalog entity - a product
    """
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['name']

    name = models.CharField(max_length=255, verbose_name=_('name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    enabled = models.BooleanField(default=True, verbose_name=_('enabled'))
    created = models.DateTimeField(auto_now_add = True, verbose_name = _('created'))
    modified = models.DateTimeField(auto_now = True, verbose_name = _('modified'))

    # categorization may differ depending on current store
    if MULTIPLE_CATEGORIES:
        categories = models.ManyToManyField(to=Category, blank=True, null=True,
            verbose_name=_('categories'), related_name='products')
    else:
        category = models.ForeignKey(to=Category, blank=True, null=True,
            verbose_name=_('category'), related_name='products')

    # pricing strategy may differ depending on current store
    if MULTIPLE_PRICES:
        @property
        def price(self):
            return Price.get_minimal_enabled_price_for_product(self)
    else:
        price = models.DecimalField(verbose_name=_('price'), max_digits=10, decimal_places=3)

    def __unicode__(self):
        return self.name

# pricing strategy may differ depending on current store
if MULTIPLE_PRICES:
    class Price(models.Model):
        """
        A Price model for advanced pricing strategy
        """
        class Meta:
            verbose_name = _('price')
            verbose_name_plural = _('prices')
            ordering = ['product', 'enabled', 'value']

        product = models.ForeignKey(to=Product, verbose_name=_('product'), related_name='prices')
        enabled = models.BooleanField(default=True, verbose_name=_('enabled'))
        value = models.DecimalField(verbose_name=_('value'), max_digits=10, decimal_places=3)
        note = models.CharField(max_length=255, verbose_name=_('note'), blank=True, null=True)

        @classmethod
        def get_minimal_enabled_price_for_product(cls, product):
            """
            Returns minimal enabled price value on set of prices related to provided product
            """
            return product.prices.filter(enabled=True).aggregate(Min('value'))['value__min']