import json
import urllib.request
import urllib.error

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import CreateView, DetailView, TemplateView, DeleteView

from .forms import ArticleForm
from .models import Article, Press
from .renderers import MarkdownRenderer


class PressListView(TemplateView):
    template_name = 'press_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = Article.objects.select_related('press').order_by('-pub_date')
        context.update(
            {
                'presses': Press.objects.prefetch_related('subscribers').all(),
                'primary_articles': articles[:5],
                'feature_articles': articles[5:9],
                'compact_articles': articles[9:15],
            }
        )
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Article.objects.select_related('press')


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '새 기사가 등록되었습니다.')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class PressSubscribeView(LoginRequiredMixin, View):
    def post(self, request, press_id):
        press = get_object_or_404(Press, id=press_id)
        user = request.user

        if press.subscribers.filter(id=user.id).exists():
            press.subscribers.remove(user)
            messages.info(request, f'{press.name} 구독을 취소했습니다.')
        else:
            press.subscribers.add(user)
            messages.success(request, f'{press.name}를 구독했습니다.')

        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(next_url or reverse_lazy('Main:press_list'))


@method_decorator(csrf_protect, name='dispatch')
class MarkdownPreviewView(LoginRequiredMixin, View):
    def post(self, request):
        content = request.POST.get('content', '')
        rendered = MarkdownRenderer.render(content)
        return JsonResponse({'html': rendered})


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_confirm_delete.html'
    success_url = reverse_lazy('Main:press_list')

    def test_func(self):
        user = self.request.user
        article = self.get_object()
        if article.author and article.author_id == user.id:
            return True
        return user.is_staff or user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, '삭제 권한이 없습니다.')
        return HttpResponseRedirect(self.get_object().get_absolute_url())

    def delete(self, request, *args, **kwargs):
        messages.info(request, '기사를 삭제했습니다.')
        return super().delete(request, *args, **kwargs)


def _zenith_request(endpoint: str, data: dict) -> dict:
    url = f"{settings.ZENITH_API_URL}{endpoint}"
    headers = {
        'X-Site-Id': settings.ZENITH_SITE_ID,
        'X-Site-Key': settings.ZENITH_SITE_KEY,
        'Content-Type': 'application/json',
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ''
        return {'error': True, 'status': e.code, 'message': error_body}
    except urllib.error.URLError as e:
        return {'error': True, 'message': str(e.reason)}


@method_decorator(csrf_exempt, name='dispatch')
class CommentUserView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        display_name = user.get_full_name() or user.username
        data = {
            'email': user.email or f'{user.username}@zenith.local',
            'username': user.username,
            'displayName': display_name,
            'profilePictureUrl': None,
            'metadata': {'djangoUserId': user.id}
        }
        result = _zenith_request('/api/comment/user', data)
        if result.get('error'):
            return JsonResponse(result, status=result.get('status', 500))
        result['displayName'] = display_name
        return JsonResponse(result)


@method_decorator(csrf_exempt, name='dispatch')
class CommentSessionView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            body = json.loads(request.body)
            user_id = body.get('userId')
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'userId required'}, status=400)

        result = _zenith_request('/api/comment/session', {'userId': user_id})
        if result.get('error'):
            return JsonResponse(result, status=result.get('status', 500))
        return JsonResponse(result)
