from django.conf.urls import patterns, url

from departureinfo import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^location=(?P<lat>\d+\.\d+),(?P<lon>\d+\.\d+),(?P<radius>\d+[\.]?\d+)$', 
        views.query, name='query'),
)
