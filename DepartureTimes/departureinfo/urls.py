from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from departureinfo import views

urlpatterns = patterns('',
                       (r'^$', TemplateView.as_view(template_name='frontend.html')),
                       url(r'^location/(?P<lat>\d+\.\d+),(?P<lon>\d+\.\d+),(?P<radius>\d+([\.]\d+)?)$',
                           views.query, name='query'),
                       url(r'^places$',
                           views.places, name='places'),

                   )
