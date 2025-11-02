from django.contrib import admin
from .models import Press, Article

@admin.register(Press)
class PressAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo')
    search_fields = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'press', 'pub_date', 'image')
    list_filter = ('press', 'pub_date')
    search_fields = ('title', 'content')