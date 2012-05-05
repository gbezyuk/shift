"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Django-admin configuration
"""
from django.utils.translation import ugettext_lazy as _
from .models import Product, Category
from modeltranslation.admin import TranslationAdmin
from doppler.base.admin import TinyMCEAdmin
from feincms.admin import tree_editor
from django.contrib import admin

class ProductAdmin(TinyMCEAdmin, TranslationAdmin):
    list_display = ('__unicode__',)

class CategoryAdmin(tree_editor.TreeEditor, TinyMCEAdmin, TranslationAdmin):
    list_display = ('__unicode__', 'enabled_toggle',)
    enabled_toggle = tree_editor.ajax_editable_boolean('enabled', _('enabled'))

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)