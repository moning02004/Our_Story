from django.contrib.auth.models import User
from django.db import models


def file_path(instance, filename):
    return '{}/{}/{}'.format(instance.post.author.username, instance.post.created.strftime('%Y-%m-%d'), filename)


class Tag(models.Model):
    keyword = models.CharField(max_length=100)

    def __str__(self):
        return self.keyword


class Heart(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(Tag)
    heart = models.ManyToManyField(Heart)

    def __str__(self):
        return self.author.username

    def heart_list(self):
        return [x.author for x in self.heart.all()]


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.ImageField(upload_to=file_path)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super(Image, self).delete(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author.username

