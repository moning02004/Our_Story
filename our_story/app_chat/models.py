from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    unread = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.content


class MessageBox(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_box_user')
    message = models.ManyToManyField(Message)
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_box_friend')

    def __str__(self):
        return '{} <--> {}'.format(self.user.username, self.friend.username)
