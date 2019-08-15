from django.contrib import admin

from app_user.models import Address
from app_chat.models import MessageByUser, Message


admin.site.register(Address)
admin.site.register(MessageByUser)
admin.site.register(Message)
