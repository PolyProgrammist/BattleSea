import django
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'riddles'


urlpatterns = [
    url(r'^$', views.createuserview, name='hello'),
    url(r'^(?P<playerid>[0-9]+)/testifplaying/$', views.testifplaying),
    url(r'^(?P<playerid>[0-9]+)/game/$', views.gameview, name='game'),
    url(r'^(?P<playerid>[0-9]+)/game/testifopponentsubmitted/$', views.testifopponentsubmitted),
    url(r'^(?P<playerid>[0-9]+)/game/(?P<row>[0-9])/(?P<col>[0-9])/hit/$', views.hitview),
    url(r'^thejsonevent/$', views.thejsonevent)
]