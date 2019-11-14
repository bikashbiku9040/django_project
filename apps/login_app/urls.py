"""import"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # page navigations
    url(r'^$', views.index),
    url(r'^success$', views.success),
    # methods
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
]
