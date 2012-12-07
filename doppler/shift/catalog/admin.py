"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Django-admin configuration
"""
import os
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _, ugettext as __
from .models import *
from modeltranslation.admin import TranslationAdmin
from doppler.base.admin import TinyMCEAdmin
from feincms.admin import tree_editor
from django.contrib import admin
from django.conf import settings
from filebrowser.base import FileObject
from rollyourown.seo.admin import get_inline
from main.seo import MyMetadata
admin.site.register(Size)

def get_image_thumbnail_html(image):
    if image:
        image_fileobject = FileObject(image.path)
        if image_fileobject and image_fileobject.filetype == "Image" \
        and os.path.isfile(settings.MEDIA_ROOT + image.path):
            str = '<img src="%s" />' % image_fileobject.version_generate(settings.FILEBROWSER_ADMIN_THUMBNAIL).url
            return str
        return False
    else:
        return False

def get_object_thumbnails_html(obj):
    html_bits = []
    for attached_image in obj.images.all():
        html_bit = get_image_thumbnail_html(attached_image.image)
        if html_bit:
            html_bits.append('<li style="float: left; margin: 2px; padding: 0;">' + html_bit + '</li>')
    if html_bits:
        return '<ul style="margin: 0; padding: 0; overflow: hidden; min-width: 168px; max-width: 336px;">' + ''.join(html_bits) + '</ul>'
    return _('no images')

class ShipmentTabularInline(admin.TabularInline):
    model = Shipment

class ImageTabularInline(generic.GenericTabularInline):
    model = Image

class ProductAdmin(TinyMCEAdmin, TranslationAdmin):
    list_display = ('lot', 'name', 'base_price', 'main_image', 'other_images', 'html_description', 'enabled', 'category', )
    list_editable = ('enabled',)
    list_display_links = ('lot', 'name', 'html_description',)
    inlines = [ImageTabularInline, get_inline(MyMetadata)]
    prepopulated_fields = {"slug": ("name",)}

    list_filter = ('category', 'enabled')

    def lot(self, object):
        return object.id
    lot.short_description = _('lot')

    def html_description(self, object):
        return object.description
    html_description.short_description = _('description')
    html_description.allow_tags = True

    def main_image(self, obj):
        if obj.main_image:
            return get_image_thumbnail_html(obj.main_image.image)
        else:
            return _('not set')
    main_image.allow_tags = True
    main_image.short_description= _('main image')

    def other_images(self, obj):
        return get_object_thumbnails_html(obj)
    other_images.allow_tags = True
    other_images.short_description= _('other images')

    list_display = ('lot', 'name', 'main_image', 'other_images', 'html_description', 'enabled',
                    'base_price','category', )
    def price(self, object):
        return object.price
    price.short_description= _('price')
    def other_prices(self, object):
        prices = object.prices.all()
        if not prices:
            return _('not set')
        html_chunk = '<ul>'
        for price in prices:
            html_chunk += '<li>%d %s %s</li>' % (price.value, __('on') if price.enabled else __('off'), price.note)
        html_chunk += '</ul>'
        return html_chunk
    other_prices.short_description= _('other prices')
    other_prices.allow_tags = True
    inlines = [ShipmentTabularInline, ImageTabularInline, get_inline(MyMetadata)]

class CategoryAdmin(tree_editor.TreeEditor, TinyMCEAdmin, TranslationAdmin):
    list_display = ('__unicode__', 'enabled_toggle', 'main_image', 'other_images', 'html_description')
    enabled_toggle = tree_editor.ajax_editable_boolean('enabled', _('enabled'))
    prepopulated_fields = {"slug": ("name",)}

    def html_description(self, object):
        return object.description
    html_description.short_description = _('description')
    html_description.allow_tags = True

    def main_image(self, obj):
        if obj.main_image:
            return get_image_thumbnail_html(obj.main_image.image)
        else:
            return _('not set')
    main_image.allow_tags = True
    main_image.short_description= _('main image')

    def other_images(self, obj):
        return get_object_thumbnails_html(obj)
    other_images.allow_tags = True
    other_images.short_description= _('other images')
    inlines = [ImageTabularInline, get_inline(MyMetadata)]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)