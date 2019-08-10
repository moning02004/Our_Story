import os

from django.contrib.auth.models import User
from django.db import models


def file_path(instance, filename):
    return 'profile_picture/{}/{}'.format(instance.user.username, filename)


class Address(models.Model):
    keyword = models.CharField(max_length=100)

    def __str__(self):
        return self.keyword


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=file_path)
    friend = models.ManyToManyField('self')
    birth = models.CharField(max_length=12, default='')
    sex = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    address_keywords = models.ManyToManyField(Address)

    # 더 추가될 수 있음

    def __str__(self):
        return "{}'s Profile".format(self.user)

    def get_name(self):
        return self.user.last_name + self.user.first_name

    def filename(self):
        return os.path.basename(self.picture.name)