"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Models implementation
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel
from .managers import EnabledTreeManager, EnabledRootManager
from django.conf import settings

try:
    MULTIPLE_CATEGORIES = settings.DOPPLER_SHIFT_CATALOG_PRODUCT_MULTIPLE_CATEGORIES
except AttributeError:
    MULTIPLE_CATEGORIES = False

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

    def __unicode__(self):
        return self.name