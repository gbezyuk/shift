"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Checkout
Part: Django-admin configuration
"""
import os
from django.utils.translation import ugettext_lazy as _, ugettext as __
from .models import Order, OrderItem
from django.contrib import admin

class OrderItemTabularInline(admin.TabularInline):
    model = OrderItem
#    readonly_fields = ['product', 'quantity',]

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTabularInline]

admin.site.register(Order, OrderAdmin)