"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Django-admin configuration
"""
from django.utils.translation import ugettext_lazy as _
from .models import Product, Category, MULTIPLE_PRICES, MULTIPLE_CATEGORIES
from modeltranslation.admin import TranslationAdmin
from doppler.base.admin import TinyMCEAdmin
from feincms.admin import tree_editor
from django.contrib import admin

if MULTIPLE_PRICES:
    from .models import Price

class PriceTabularInline(admin.TabularInline):
    model = Price

class ProductAdmin(TinyMCEAdmin, TranslationAdmin):
    list_display = ('lot', 'name', 'description', 'enabled', 'price', 'category', )
    list_editable = ('enabled',)
    list_display_links = ('lot', 'name', 'description',)

    if MULTIPLE_CATEGORIES:
        list_display = ('pk', 'enabled', 'name', 'price', )

    if MULTIPLE_PRICES:
        def price(self, object):
            return object.price
        price.short_description = _('price')
        inlines = [PriceTabularInline]

    def lot(self, object):
        return object.id
    lot.short_description = _('lot')

class CategoryAdmin(tree_editor.TreeEditor, TinyMCEAdmin, TranslationAdmin):
    list_display = ('__unicode__', 'enabled_toggle',)
    enabled_toggle = tree_editor.ajax_editable_boolean('enabled', _('enabled'))

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)