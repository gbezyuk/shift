"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Models implementation
"""
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.aggregates import Min
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel
from .managers import EnabledTreeManager, EnabledRootManager
from django.conf import settings
from filebrowser.fields import FileBrowseField
from django.forms import ValidationError
from pytils.translit import slugify

try:
    MULTIPLE_CATEGORIES = settings.DOPPLER_SHIFT_CATALOG_PRODUCT_MULTIPLE_CATEGORIES
except AttributeError:
    MULTIPLE_CATEGORIES = False
try:
    MULTIPLE_PRICES = settings.DOPPLER_SHIFT_CATALOG_PRODUCT_MULTIPLE_PRICES
except AttributeError:
    MULTIPLE_PRICES = False

class Image(models.Model):
    title = models.CharField(max_length=500, unique=False, blank=True, null=True, verbose_name=_('title'))
    enabled = models.BooleanField(default=True, verbose_name=_('enabled'))
    priority = models.BooleanField(default=False, verbose_name=_('priority'))
    image = FileBrowseField(max_length=500, extensions=[".jpeg", ".jpg",".png", ".gif"], blank=False, null=False, verbose_name=_('image'))
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')
        ordering = ['title']

    @classmethod
    def get_main_image_for_object(cls, object):
        #TODO: rewrite with better generic fields usage
        if object.images.filter(enabled=True, priority=True).exists():
            return object.images.filter(enabled=True, priority=True).order_by('?')[0]
        elif object.images.filter(enabled=True).exists():
            return object.images.filter(enabled=True).order_by('?')[0]
        return None

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
    images = generic.GenericRelation(Image, verbose_name=_('images'), blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name=_('slug'))

    @property
    def main_image(self):
        self_main = Image.get_main_image_for_object(self)
        if self_main:
            return self_main
        if self.products.all().exists():
            for product in self.products.all().order_by('?'):
                product_image = product.main_image
                if product_image:
                    return product_image
        for child in self.children.filter(enabled=True):
            if child.main_image:
                return child.main_image
        return None
    created = models.DateTimeField(auto_now_add = True, verbose_name = _('created'))
    modified = models.DateTimeField(auto_now = True, verbose_name = _('modified'))

    enabled_tree = EnabledTreeManager()
    enabled_root = EnabledRootManager()

    @property
    def enabled_products(self):
        return self.products.filter(enabled=True)

    @property
    def enabled_children(self):
        return self.children.filter(enabled=True)

    @property
    def topmost_parent(self):
        parent = self.parent
        if not parent:
            return None
        while parent.parent:
            parent = parent.parent
        return parent

    @property
    def is_inside_disabled_parent(self):
        parent = self.parent
        while parent:
            if not parent.enabled:
                return True
            parent = parent.parent
        return False

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

#    @models.permalink
    def get_absolute_url(self):
#        return 'doppler_shift_catalog_category', (), {'category_id': self.pk}
        return '/%s/' % self.slug

    def has_active_children(self):
        return Category.objects.filter(parent=self, enabled=True).exists()

    def active_children(self):
        return Category.objects.filter(parent=self, enabled=True)

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
    images = generic.GenericRelation(Image, verbose_name=_('images'), blank=True, null=True)
    slug = models.SlugField(unique=True, verbose_name=_('slug'), max_length=255)
    you_might_be_interested = models.ManyToManyField(to='self', verbose_name=_('You might be interested'), null=True, blank=True)
    also_they_buy_with_this_product = models.ManyToManyField(to='self', verbose_name=_('Also they buy with this product'), null=True, blank=True)

    @property
    def enabled_images(self):
        return self.images.filter(enabled=True)
    @property
    def main_image(self):
        return Image.get_main_image_for_object(self)
    created = models.DateTimeField(auto_now_add = True, verbose_name = _('created'))
    modified = models.DateTimeField(auto_now = True, verbose_name = _('modified'))

    # categorization may differ depending on current store
    if MULTIPLE_CATEGORIES:
        categories = models.ManyToManyField(to=Category, blank=True, null=True,
            verbose_name=_('categories'), related_name='products')
    else:
        category = models.ForeignKey(to=Category, blank=True, null=True,
            verbose_name=_('category'), related_name='products')

        @property
        def is_inside_disabled_parent(self):
            if not self.category:
                return False
            return (not self.category.enabled) or self.category.is_inside_disabled_parent

    # pricing strategy may differ depending on current store
    if MULTIPLE_PRICES:
        def get_minimal_enabled_price(self):
            return Price.get_minimal_enabled_price_for_product(self)
        @property
        def price(self):
            price_obj = self.get_minimal_enabled_price()
            return price_obj.value if price_obj else None
        @property
        def remainder(self):
            price_obj = self.get_minimal_enabled_price()
            return price_obj.remainder if price_obj else None
        @property
        def remainder_update_time(self):
            price_obj = self.get_minimal_enabled_price()
            return price_obj.modified if price_obj else None
    else:
        price = models.PositiveIntegerField(verbose_name=_('price'), default=0)
        remainder = models.PositiveIntegerField(verbose_name=_('remainder'), default=0)
        @property
        def remainder_update_time(self):
            return self.modified

    def you_might_be_interested_enabled_products(self):
        return self.you_might_be_interested.filter(enabled=True)

    def also_they_buy_with_this_product_enabled_products(self):
        return self.also_they_buy_with_this_product.filter(enabled=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Product, self).save(*args, **kwargs)

#    @models.permalink
    def get_absolute_url(self):
#        return 'doppler_shift_catalog_product', (), {'product_id': self.pk}
        return '/%s/' % self.slug

# pricing strategy may differ depending on current store
if MULTIPLE_PRICES:
    class Price(models.Model):
        """
        A Shipment model for advanced pricing strategy
        """
        class Meta:
            verbose_name = _('shipment')
            verbose_name_plural = _('shipments')
            ordering = ['product', 'enabled', 'value']
            unique_together = [('product', 'value',),]

        product = models.ForeignKey(to=Product, verbose_name=_('product'), related_name='prices')
        enabled = models.BooleanField(default=True, verbose_name=_('enabled'))
        remainder = models.PositiveIntegerField(verbose_name=_('remainder'), default=0)
        value = models.PositiveIntegerField(verbose_name=_('price'))
        added_to_cart_times = models.PositiveIntegerField(verbose_name=_('added to cart times'), default=0)
        ordered_times = models.PositiveIntegerField(verbose_name=_('ordered times'), default=0)
        note = models.CharField(max_length=255, verbose_name=_('note'), blank=True, null=True)
        created = models.DateTimeField(auto_now_add = True, verbose_name = _('created'))
        modified = models.DateTimeField(auto_now = True, verbose_name = _('modified'))

        @classmethod
        def get_minimal_enabled_price_for_product(cls, product):
            """
            Returns minimal enabled price value on set of prices related to provided product
            """
            min_value = product.prices.filter(enabled=True).aggregate(Min('value'))['value__min']
            if min_value:
                return product.prices.filter(enabled=True, value=min_value)[0]
            return None

        def __unicode__(self):
            return "%r - %s" % (self.product.name, self.value)

        def decrease_remainer(self, quantity):
            assert quantity <= self.remainder
            self.remainder -= quantity
            self.save()

class ProductNotAvailableError(ValidationError):
    """
    Product not available error for cases when someone wants too much of anything
    """
    def __init__(self, message, product, shipment, requested_quantity, maximal_available_quantity):
        super(ProductNotAvailableError, self).__init__(message=message)
        self.product = product
        self.shipment = shipment
        self.requested_quantity = requested_quantity
        self.maximal_available_quantity = maximal_available_quantity