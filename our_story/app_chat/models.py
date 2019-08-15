from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='From_User')
    content = models.TextField()
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='To_User')
    created = models.DateTimeField(auto_now=True)
    unread = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.content


class MessageByUser(models.Model):
    participant = models.TextField()
    message = models.ManyToManyField(Message)

    def __str__(self):
        return '{}'.format(self.participant)
