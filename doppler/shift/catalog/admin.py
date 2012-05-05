"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Django-admin configuration
"""
from .models import Product, Category

from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)