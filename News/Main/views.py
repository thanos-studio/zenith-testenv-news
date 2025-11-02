from django.shortcuts import render , get_object_or_404,redirect
from .models import Press, Article
from .forms import ArticleForm 

def home(request):
    return render(request, 'home.html')

def press_list(request):
    presses = Press.objects.all()
    articles = Article.objects.all().order_by('-pub_date')  # 최신 순
    return render(request, 'press_list.html', {'presses': presses, 'articles': articles})

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'article_detail.html', {'article': article})

def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Main:press_list')  # 작성 후 돌아갈 페이지
    else:
        form = ArticleForm()
    return render(request, 'article_form.html', {'form': form})

def subscribe(request, press_id):
    press = get_object_or_404(Press, id=press_id)
    if request.user.is_authenticated:
        if request.user in press.subscribers.all():
            press.subscribers.remove(request.user)  # 이미 구독하면 취소
        else:
            press.subscribers.add(request.user)     # 구독 추가
    return redirect('Main:press_list')  # 다시 돌아가기