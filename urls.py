from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
     url(r'^order$', 'LunchOrder.views.OrderPage'),
     url(r'^order/submit/$','LunchOrder.views.SubmitOrder'),	    
     url(r'^order/confirm/$','LunchOrder.views.Confirm'),
     url(r'^index','LunchOrder.views.Index'),
     url(r'^view','LunchOrder.views.OrdersView'),
     url(r'^login','LunchOrder.views.Login'),
     url(r'^logout','LunchOrder.views.Logout'),
     url(r'^newuser','LunchOrder.views.NewUser'),
     url(r'^createuser','LunchOrder.views.CreateUser'),
     url(r'^kitchen','LunchOrder.views.Kitchen'),
     url(r'^(?P<order_id>\d+)/$','LunchOrder.views.OrderDetail'),
     url(r'^(?P<order_id>\d+)/fill','LunchOrder.views.FillOrder'),
     url(r'^(?P<order_id>\d+)/cancel','LunchOrder.views.CancelOrder'),
    # url(r'^BrownBoxApp/', include('BrownBoxApp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
