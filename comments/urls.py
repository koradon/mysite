from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<id>\d+)/$', views.comment_thread, name="thread"),
    # url(r'^(?P<id>[\w-]+)/delete/$', comment_delete, name="delete"),
]