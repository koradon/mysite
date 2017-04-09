from django.conf.urls import url

from . import views
from .feeds import LatestPostFeed


urlpatterns = [
    #url(r'^$', views.index, name="index"),
    url(r'^$', views.post_list, name="list"),
    url(r'^feed/$', LatestPostFeed(), name='post_feed'),
    url(r'^create/$', views.post_create, name="create"),
    url(r'^(?P<slug>[\w-]+)/$', views.post_detail, name="detail"),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update, name="update"),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.post_delete, name="delete"),
    url(r'^(?P<slug>[\w-]+)/share/$', views.post_share, name="share"),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name="list_by_tags"),
]
