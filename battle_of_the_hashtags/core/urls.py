from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^get_battle/(?P<pk>[0-9]+)/$', views.get_battle, name="get_battle"),
]
