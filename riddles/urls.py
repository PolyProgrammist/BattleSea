import django
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'riddles'


urlpatterns = [
    url(r'^$', views.helloview, name='hello'),
    url(r'^game/$', views.gameview, name='game'),
    url(r'^(?P<row>[0-9])/(?P<col>[0-9])/hit/$', views.hitview),
    url(r'^game/(?P<playerid>[0-9]+)/showid/$', views.testshowid)
]