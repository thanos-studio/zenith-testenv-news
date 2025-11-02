from django.db import models
from django.contrib.auth.models import User

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
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='article_images/', blank=True, null=True)

    def __str__(self):
        return self.title