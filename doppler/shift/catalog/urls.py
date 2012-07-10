"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: url set
"""
from django.conf.urls.defaults import patterns, include, url
from .views import index#, category, product

urlpatterns = patterns('',
    url(r'^$', index, name='doppler_shift_catalog_index'),
#    url(r'^category/(?P<category_id>\d+)/$', category, name='doppler_shift_catalog_category'),
#    url(r'^(?P<product_id>\d+)/$', product, name='doppler_shift_catalog_product'),
    # using fallback middlewares now
)