from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from django.views import View
from study_admin.models import *
from study_admin.forms import *
# Create your views here.

class Login(View):
    def get(self, request, *args, **kwargs):
        if User.login_user_is_admin(request):
            return redirect(reverse('admin:index'))
        if User.now_login(request):
            return redirect(reverse('user:redirect_first_article'))
        context = {
            'redirect_to': request.GET.get('redirect_to', reverse('admin:login')),
        }
        return render(request, 'admin/login.html', context)
    def post(self, request, *args, **kwargs):
        if User.login_user_is_admin(request):
            return redirect(reverse('admin:index'))
        if User.now_login(request):
            return redirect(reverse('user:redirect_first_article'))
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        redirect_to = request.GET.get('redirect_to', reverse('admin:login'))
        context = {
            'username': username,
            'redirect_to': redirect_to,
        }
        if not username or not password:
            context['error_msg'] = '모든 필드를 채워주세요'
            return render(request, 'admin/login.html', context)
        login_result = User.set_login(request, username, password)
        if not login_result[0]:
            context['error_msg'] = login_result[1]
            return render(request, 'admin/login.html', context)
        return redirect(redirect_to)


class Join(View):
    def get(self, request, *args, **kwargs):
        if User.login_user_is_admin(request):
            return redirect(reverse('admin:index'))
        if User.now_login(request):
            return redirect(reverse('user:redirect_first_article'))
        return render(request, 'admin/join.html')
    def post(self, request, *args, **kwargs):
        if User.login_user_is_admin(request):
            return redirect(reverse('admin:index'))
        if User.now_login(request):
            return redirect(reverse('user:redirect_first_article'))
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        context = {
            'username': username,
        }
        if not username or not password or not password_confirm:
            context['error_msg'] = '모든 필드를 채워주세요'
            return render(request, 'admin/join.html', context)
        if password != password_confirm:
            context['error_msg'] = '패스워드를 다시 확인해주세요'
            return render(request, 'admin/join.html', context)
        join_result = User.create_user(username, password)
        if not join_result[0]:
            context['error_msg'] = join_result[1]
            return render(request, 'admin/join.html', context)
        return redirect(reverse('admin:login'))


class Logout(View):
    def get(self, request, *args, **kwargs):
        User.set_logout(request)
        return redirect(reverse('admin:login'))


class Index(View):
    def get(self, request, *args, **kwargs):
        if not User.login_user_is_admin(request):
            return redirect(reverse('admin:login'))
        article_qs = Article.objects.all()
        context = {
            'article_list': article_qs.order_by('chapter'),
            'login_user': User.get_login_user(request),
            'article_list_active': 'active',
        }
        return render(request, 'admin/index.html', context)


class New(View):
    def get(self, request, *args, **kwargs):
        if not User.login_user_is_admin(request):
            return redirect(reverse('admin:login'))
        context = {
            'login_user': User.get_login_user(request),
            'article_list_active': 'active',
        }
        return render(request, 'admin/new.html', context)
    def post(self, request, *args, **kwargs):
        if not User.login_user_is_admin(request):
            return redirect(reverse('admin:login'))
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            chapter = article_form.cleaned_data['chapter']
            title = article_form.cleaned_data['title']
            content = article_form.cleaned_data['content']
            article = Article(
                chapter=chapter,
                title=title,
                content=content,
            )
            article.save()
            return redirect(reverse('admin:detail', kwargs={'article_id':article.id}))
        else:
            context = {
                'article': article_form.cleaned_data,
                'login_user': User.get_login_user(request),
                'error_msg': '입력값이 올바르지 않습니다',
                'article_list_active': 'active',
            }
            return render(request, 'admin/new.html', context)


class Detail(View):
    def get(self, request, *args, **kwargs):
        if not User.login_user_is_admin(request):
            return redirect(reverse('admin:login'))
        article = get_object_or_404(Article, pk=kwargs.get('article_id'))
        context = {
            'article': article,
            'login_user': User.get_login_user(request),
            'article_list_active': 'active',
        }
        return render(request, 'admin/detail.html', context)


class Modify(View):
    def get(self, request, *args, **kwargs):
        if not User.login_user_is_admin(request):
            return redirect(reverse('admin:login'))
        article = get_object_or_404(Article, pk=kwargs.get('article_id'))
        context = {
            'article': article,
            'login_user': User.get_login_user(request),
            'article_list_active': 'active',
        }
        return render(request, 'admin/modify.html', context)
    def post(self, request, *args, **kwargs):
        if not User.login_user_is_admin(request):
            return redirect(reverse('admin:login'))
        article = get_object_or_404(Article, pk=kwargs.get('article_id'))
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article.chapter = article_form.cleaned_data['chapter']
            article.title = article_form.cleaned_data['title']
            article.content = article_form.cleaned_data['content']
            article.save()
            return redirect(reverse('admin:detail', kwargs={'article_id':article.id}))
        else:
            context = {
                'article': article_form.cleaned_data,
                'login_user': User.get_login_user(request),
                'error_msg': '입력값이 올바르지 않습니다',
                'article_list_active': 'active',
            }
            return render(request, 'admin/modify.html', context)


class VisibleChange(View):
    def get(self, request, *args, **kwargs):
        if not User.login_user_is_admin(request):
            return redirect(reverse('admin:login'))
        article = get_object_or_404(Article, pk=kwargs.get('article_id'))
        if not request.is_ajax():
            return redirect(reverse('admin:modify', kwargs={'article_id':article.id}))
        change_to = True
        if article.is_visible:
            change_to = False
            article.is_visible = False
        else:
            change_to = True
            article.publish()
        article.save()
        return HttpResponse(str(change_to))


class Delete(View):
    def get(self, request, *args, **kwargs):
        if not User.login_user_is_admin(request):
            return redirect(reverse('admin:login'))
        article = get_object_or_404(Article, pk=kwargs.get('article_id'))
        context = {
            'article': article,
            'delete_check_msg': article.title[:8],
            'login_user': User.get_login_user(request),
            'article_list_active': 'active',
        }
        return render(request, 'admin/delete.html', context)
    def post(self, request, *args, **kwargs):
        if not User.login_user_is_admin(request):
            return redirect(reverse('admin:login'))
        article = get_object_or_404(Article, pk=kwargs.get('article_id'))
        if article.title[:8] == request.POST.get('delete_check_msg'):
            article.delete()
            return redirect(reverse('admin:index'))
        else:
            context = {
                'article': article,
                'delete_check_msg': article.title[:8],
                'login_user': User.get_login_user(request),
                'error_msg': '삭제 확인 메시지를 정확하게 입력해주세요',
                'article_list_active': 'active',
            }
            return render(request, 'admin/delete.html', context)


class UserIndex(View):
    def get(self, request, *args, **kwargs):
        if not User.login_user_is_admin(request):
            return redirect(reverse('admin:login'))
        user_qs = User.objects.all()
        context = {
            'user_list': user_qs,
            'login_user': User.get_login_user(request),
            'user_list_active': 'active',
        }
        return render(request, 'admin/user_index.html', context)


class UserDelete(View):
    def delete(self, request, *args, **kwargs):
        if not User.login_user_is_admin(request):
            return HttpResponse('forbidden', status=403)
        if request.is_ajax():
            user = get_object_or_404(User, pk=kwargs.get('user_id'))
            user.delete()
            return HttpResponse('ok.')


class UserChangeValid(View):
    def put(self, request, *args, **kwargs):
        if not User.login_user_is_admin(request):
            return HttpResponse('forbidden', status=403)
        if request.is_ajax():
            user = get_object_or_404(User, pk=kwargs.get('user_id'))
            change_to = True
            if user.is_valid:
                user.is_valid = False
                change_to = False
            else:
                user.is_valid = True
                change_to = True
            user.save()
            return HttpResponse(change_to)
