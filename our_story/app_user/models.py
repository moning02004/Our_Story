import os

from django.contrib.auth.models import AbstractUser
from django.db import models


def file_path(instance, filename):
    return 'avatar/{}/{}'.format(instance.username, filename)


class User(AbstractUser):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to=file_path, null=True, blank=True)
    tel = models.CharField(max_length=13)
    gender = models.CharField(max_length=10, null=True, blank=True)
    birth = models.DateTimeField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True, default='')
    status = models.CharField(max_length=150, default='')
    friend = models.ManyToManyField('self')

    def __str__(self):
        return "{}'s Profile".format(self.name)

    def filename(self):
        return os.path.basename(self.avatar.name)


class Notice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notice_to_user')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notice_from_user')
    content = models.TextField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
