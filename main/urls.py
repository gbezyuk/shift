from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from filebrowser.sites import site
from django.conf import settings
from .views import *
admin.autodiscover()

handler404 = ViewFor404.as_view()
handler500 = ViewFor500.as_view()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/rosetta/', include('rosetta.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^', include('doppler.shift.urls')),
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