from django.conf.urls import url
from study_admin.views import *

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^new/$', New.as_view(), name='new'),
    url(r'^(?P<article_id>\d+)/$', Detail.as_view(), name='detail'),
    url(r'^(?P<article_id>\d+)/modify/$', Modify.as_view(), name='modify'),
    url(r'^(?P<article_id>\d+)/modify/visible/$', VisibleChange.as_view(), name='visible_change'),
    url(r'^(?P<article_id>\d+)/delete/$', Delete.as_view(), name='delete'),
    url(r'^users/$', UserIndex.as_view(), name='user_index'),
    url(r'^users/(?P<user_id>\d+)/$', UserDelete.as_view(), name='user_delete'),
    url(r'^users/(?P<user_id>\d+)/modify/valid/$', UserChangeValid.as_view(), name='user_change_valid'),
]