"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Checkout
Part: url set
"""
from django.conf.urls import patterns, url
from .views import cart, clear_cart, make_order, orders, order

urlpatterns = patterns('',
    url(r'^cart/$', cart, name='doppler_shift_cart'),
    url(r'^cart/clear$', clear_cart, name='doppler_shift_clear_cart'),
    url(r'^cart/order', make_order, name='doppler_shift_make_order'),
    url(r'^orders/$', orders, name='doppler_shift_orders'),
    url(r'^orders/(?P<order_id>\d+)$', order, name='doppler_shift_order'),
)
