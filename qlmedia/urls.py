from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'qlmedia.views.home', name='home'),
    # url(r'^qlmedia/', include('qlmedia.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ajax_upload/$', 'transcode.views.ajax_upload'),
    url(r'^play/$', 'transcode.views.play'),
    url(r'^get_status/$', 'transcode.views.get_status'),
    url(r'^get_encode_progress/$', 'transcode.views.get_encode_progress'),
    url(r'^get_transfer_progress/$', 'transcode.views.get_transfer_progress'),
    #(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/leen/media'}),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
