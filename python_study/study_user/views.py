from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.urls import reverse
from django.views import View
from study_admin.models import *
# Create your views here.

class RedirectFirstArticle(View):
    def get(self, request, *args, **kwargs):
        article = Article.objects.filter(is_visible=True).order_by('chapter').first()
        return redirect(reverse('user:article_view', kwargs={'article_id':article.id}))


class ArticleView(View):
    def get(self, request, *args, **kwargs):
        if not User.now_login(request):
            return redirect(reverse('admin:login'))
        article = get_object_or_404(Article, pk=kwargs.get('article_id'))
        if not article.is_visible:
            raise Http404
        article_qs = Article.objects.filter(is_visible=True).order_by('chapter')
        context = {
            'article': article,
            'article_list': article_qs,
        }
        return render(request, 'user/view.html', context)
