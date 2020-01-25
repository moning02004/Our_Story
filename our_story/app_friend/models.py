from django.db import models

from app_user.models import User


class MaybeKnow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maybe')
    someone = models.ForeignKey(User, on_delete=models.CASCADE, related_name='someone')

    def __str__(self):
        return self.user.name + '의 지인 : ' + self.someone.name