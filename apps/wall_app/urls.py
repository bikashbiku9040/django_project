"""import"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # page navigations
    url(r'^wall$', views.wall),
    # methods
    url(r'^create_message$', views.create_message),
    url(r'^create_comment$', views.create_comment),
    url(r'^remove_message/(?P<number>\d+)$', views.remove_message),
    url(r'^remove_comment/(?P<number>\d+)$', views.remove_comment),
]
