from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from .renderers import MarkdownRenderer

# Create your models here.
class Press(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='press_logos/', blank=True, null=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='subscribed_presses')

    def __str__(self):
        return self.name


class Article(models.Model):
    press = models.ForeignKey(Press, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=200)
    content = models.TextField(help_text='Markdown 형식으로 내용을 작성하세요.')
    pub_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='article_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')

    def __str__(self):
        return self.title

    @property
    def rendered_content(self) -> str:
        return MarkdownRenderer.render(self.content)

    def get_absolute_url(self):
        return reverse('Main:article_detail', args=[self.pk])
