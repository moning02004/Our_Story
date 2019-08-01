from django.contrib.auth.models import User
from django.db import models


# common models
class Tag(models.Model):
    keyword = models.CharField(max_length=100)

    def __str__(self):
        return self.keyword


class Heart(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.author


class Comment(models.Model):
    author = models.CharField(max_length=100)
    content = models.CharField(max_length=100)

    def __str__(self):
        return self.author
