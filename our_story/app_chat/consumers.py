from channels.generic.websocket import AsyncWebsocketConsumer
import json

from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Q, Sum

from .models import MessageBox, Message


class ChatConsumer(AsyncWebsocketConsumer):

    __channels_list = dict()
    __member_list = list()
    async def connect(self):
        self.friend = self.scope['url_route']['kwargs']['friend']
        self.me = self.scope['url_route']['kwargs']['me']

        self.participant = [self.friend, self.me]
        self.participant.sort()
        self.participant = '_'.join(self.participant)

        await self.channel_layer.group_add(
            self.participant,
            self.channel_name
        )

        self.__member_list.append(self.me) if not self.me in self.__member_list else None
        self.__channels_list[self.participant] = self.__member_list

        await self.accept()
        await self.channel_layer.group_send(
            self.participant,
            {
                'type': 'init_channel',
                'q': 'Accept',
                'left': len(self.__channels_list[self.participant]) == 1,
            })

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.participant,
            self.channel_name
        )
        try:
            self.__channels_list[self.participant].remove(self.me)
        except:
            pass

    async def receive(self, text_data):
        left = len(self.__channels_list[self.participant]) == 1

        text_data_json = json.loads(text_data)
        user = User.objects.get(username=self.me)
        friend = User.objects.get(username=self.friend)

        message = Message.objects.create(
            content=text_data_json['content'],
            from_user=User.objects.get(username=self.me),
            to_user=User.objects.get(username=self.friend)
        )
        if not left:
            message.unread = 0
            message.save()

        for x, y in [[user, friend], [friend, user]]:
            query = Q(user=x) & Q(friend=y)
            message_box = MessageBox.objects.get(query)
            message_box.message.add(message)
            message_box.last_time = message.created

        message_box = MessageBox.objects.get(Q(user=friend) & Q(friend=user))
        unread = message_box.message.all().filter(to_user=friend).aggregate(sum=Sum('unread'))['sum']
        await self.channel_layer.group_send(
            self.participant,
            {
                'type': 'chat_message',
                'content': message.content,
                'from_user': message.from_user.username,
                'to_user': message.to_user.profile.get_name(),
                'created': message.created.strftime('%H:%M'),
                'left': left
            }
        )
        await self.channel_layer.group_send(
            self.friend,
            {
                'type': 'refresh',
                'content': message.content,
                'user': message.from_user.username,
                'unread': unread
            }
        )
        await self.channel_layer.group_send(
            self.me,
            {
                'type': 'refresh',
                'content': message.content,
                'user': message.to_user.username,
                'unread': 0
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'content': event['content'],
            'from_user': event['from_user'],
            'to_user': event['to_user'],
            'created': event['created'],
            'left': event['left']
        }))

    async def init_channel(self, event):
        await self.send(text_data=json.dumps({
            'q': event['q'],
            'left': event['left']
        }))