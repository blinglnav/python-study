from django.conf.urls import url
from study_user.views import *

urlpatterns = [
    url(r'^$', RedirectFirstArticle.as_view(), name='redirect_first_article'),
    url(r'^(?P<article_id>\w+)/$', ArticleView.as_view(), name='article_view'),
]