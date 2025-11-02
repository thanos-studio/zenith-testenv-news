from django.shortcuts import render , get_object_or_404,redirect
from .models import Press, Article

def home(request):
    return render(request, 'home.html')

def press_list(request):
    presses = Press.objects.all()
    articles = Article.objects.all().order_by('-pub_date')  # 최신 순
    return render(request, 'press_list.html', {'presses': presses, 'articles': articles})

def subscribe(request, press_id):
    press = get_object_or_404(Press, id=press_id)
    # 구독 로직 구현 (예: request.user가 구독 리스트에 추가)
    # 예시: request.user.subscriptions.add(press)
    return redirect('press_list')  # 구독 후 메인 페이지로 돌아가기

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'article_detail.html', {'article': article})
