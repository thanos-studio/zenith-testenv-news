from django.urls import path

from .views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    MarkdownPreviewView,
    PressListView,
    PressSubscribeView,
)

app_name = 'Main'

urlpatterns = [
    path('', PressListView.as_view(), name='press_list'),
    path('subscribe/<int:press_id>/', PressSubscribeView.as_view(), name='subscribe'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('markdown/preview/', MarkdownPreviewView.as_view(), name='markdown_preview'),
]
