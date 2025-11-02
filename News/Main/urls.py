from django.urls import path
from . import views

app_name = 'Main' 

urlpatterns = [
    path('', views.press_list, name='press_list'),
    path('subscribe/<int:press_id>/', views.subscribe, name='subscribe'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('articles/create/', views.article_create, name='article_create'),
]