from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^catalog/', include('doppler.shift.catalog.urls')),
)