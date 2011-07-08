from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
     url(r'^order$', 'LunchOrder.views.Order'),
     url(r'^order/submit/$','LunchOrder.views.SubmitOrder'),	    
    # url(r'^BrownBoxApp/', include('BrownBoxApp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
