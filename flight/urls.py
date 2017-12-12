from django.conf.urls import url

from . import views

app_name = 'flight'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^delete/(?P<index>[0-9]+)/$', views.delete, name='delete'),
    url(r'^up/(?P<index>[0-9]+)/$', views.up, name='up'),
    url(r'^down/(?P<index>[0-9]+)/$', views.down, name='down'),
    url(r'^filter/$', views.filter, name='filter'),
]