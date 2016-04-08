from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^map', views.map, name="map"),
    url(r'^timeline', views.timeline, name="timeline"),
    url(r'^graph', views.graph, name="graph"),
    url(r'^upvote/(?P<photo_id>[0-9]+)/$', views.upvote, name='upvote'),
    url(r'^downvote/(?P<photo_id>[0-9]+)/$', views.downvote, name='downvote')

]
