from django.conf.urls import patterns, include, url
from views import targetScan, download

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'targetscan.views.targetScan', name='targetScan'),
    url(r'^download/([-\w]+)/$', "targetscan.views.download"),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
