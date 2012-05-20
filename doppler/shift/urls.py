from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    url(r'^catalog/', include('doppler.shift.catalog.urls')),
    url(r'^', include('doppler.shift.checkout.urls')),
    url(r'^$', redirect_to, {'url': '/catalog/', 'permanent': False}),
)