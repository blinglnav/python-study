from django.conf.urls import url
from study_admin.views import *

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^join/$', Join.as_view(), name='join'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^new/$', New.as_view(), name='new'),
    url(r'^(?P<article_id>\d+)/$', Detail.as_view(), name='detail'),
    url(r'^(?P<article_id>\d+)/modify/$', Modify.as_view(), name='modify'),
    url(r'^(?P<article_id>\d+)/delete/$', Delete.as_view(), name='delete'),
]