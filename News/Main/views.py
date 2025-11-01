from django.shortcuts import render , get_object_or_404
from .models import Press, Article

def home(request):
    return render(request, 'home.html')

def press_list(request):
    presses = Press.objects.all()
    return render(request, 'press_list.html', {'presses': presses})

def article_list(request, press_id):
    press = get_object_or_404(Press, id=press_id)
    articles = press.articles.all().order_by('-pub_date')
    return render(request, 'article_list.html', {'press': press, 'articles': articles})

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'article_detail.html', {'article': article})
