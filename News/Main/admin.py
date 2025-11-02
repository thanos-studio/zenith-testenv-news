from django.contrib import admin
from .models import Press, Article

@admin.register(Press)
class PressAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo')  # 목록에서 보여줄 필드
    search_fields = ('name',)        # 검색 가능

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'press', 'pub_date')
    list_filter = ('press', 'pub_date')  # 필터 기능
    search_fields = ('title', 'content')