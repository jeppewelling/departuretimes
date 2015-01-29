from django.conf.urls import patterns, url

from departureinfo import views

urlpatterns = patterns('',
    url(r'^lat=(?P<lat>\d+)&lon=(?P<lon>\d+)$', views.query, name='query'),
)
