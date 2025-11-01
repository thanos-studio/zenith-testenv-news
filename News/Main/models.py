from django.db import models

# Create your models here.
class Press(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='press_logos/', blank=True, null=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    press = models.ForeignKey(Press, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title