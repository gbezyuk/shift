from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from filebrowser.sites import site
from django.conf import settings
from django.views.generic.simple import redirect_to
from .views import *
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/rosetta/', include('rosetta.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('doppler.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
#    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^$', redirect_to, {'url': '/mens-wear/', 'permanent': False}),
    url(r'^', include('doppler.shift.urls')),

    url(r'^mens-wear/$', mens),
    url(r'^womens-wear/$', womens),
    url(r'^children-wear/$', children),
    url(r'^to-customer/$', to_customer),
    url(r'^contacts/$', contacts),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve',
			 {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	)
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve',
			 {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
	)
