from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^lists/the_only_list_in_the_world/$', 'lists.views.view_list', name='view_list'),
    url(r'^admin/', include(admin.site.urls)),
)
