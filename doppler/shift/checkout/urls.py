"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Checkout
Part: url set
"""
from django.conf.urls.defaults import patterns, url
from .views import cart

urlpatterns = patterns('',
    url(r'^cart/$', cart, name='doppler_shift_cart'),
)