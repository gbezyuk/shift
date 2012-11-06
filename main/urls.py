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
    url(r'^accounts/', include('social_auth.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', home, name='home'),
    url(r'^', include('doppler.shift.urls')),
    url(r'^googleca70414f1dff2fd9.html$', google_site_verification),

    url(r'^robokassa/', include('robokassa.urls')),
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
