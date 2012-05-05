"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Models implementation
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel

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

    def __unicode__(self):
        return self.name

class Category(MPTTModel):
    """
    Basic catalog entity - a category
    """
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['tree_id', 'lft'] # ordering like that is a django-mptt requirement, as far as I know @gb
    name = models.CharField(max_length=255, verbose_name=_('name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    enabled = models.BooleanField(default=True, verbose_name=_('enabled'))
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_('parent'))
    created = models.DateTimeField(auto_now_add = True, verbose_name = _('created'))
    modified = models.DateTimeField(auto_now = True, verbose_name = _('modified'))

    def __unicode__(self):
        return self.name