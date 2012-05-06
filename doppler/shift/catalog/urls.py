"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: url set
"""
from django.conf.urls.defaults import patterns, include, url
from .views import index, category

urlpatterns = patterns('',
    url(r'^$', index, name='doppler_shift_catalog_index'),
    url(r'^(?P<category_id>\d+)/$', category, name='doppler_shift_catalog_category'),
)