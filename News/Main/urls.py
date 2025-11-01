from django.urls import path
from . import views

urlpatterns = [
    path('', views.press_list, name='press_list'),
    path('<int:press_id>/', views.article_list, name='article_list'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
]