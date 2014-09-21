from django.conf.urls import patterns, include, url
from person import views


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'foodbar.views.home', name='home'),
    # url(r'^foodbar/', include('foodbar.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', views.main, name='main'),
    url(r'^personalized/', views.get_personalized_selection, name='personalized'),
    url(r'^all/', views.list_all_businesses, name='all-businesses'),
)
