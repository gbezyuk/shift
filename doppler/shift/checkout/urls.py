"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Checkout
Part: url set
"""
from django.conf.urls import patterns, url
from .views import cart, clear_cart

urlpatterns = patterns('',
    url(r'^cart/$', cart, name='doppler_shift_cart'),
    url(r'^cart/clear$', clear_cart, name='doppler_shift_clear_cart'),
)