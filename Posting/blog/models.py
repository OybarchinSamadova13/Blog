from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to="images/")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    content = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment', )
    date_commented = models.DateTimeField(auto_now=True)
