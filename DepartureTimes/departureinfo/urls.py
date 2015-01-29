from django.conf.urls import patterns, url

from departureinfo import views

urlpatterns = patterns('',
    url(r'^(?P<lat>\d+)/(?P<lon>\d+)$', views.query, name='query'),
)
