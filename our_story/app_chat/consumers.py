from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.contrib.auth.models import User
from django.db.models import Q

from .models import MessageByUser, Message


class ChatConsumer(AsyncWebsocketConsumer):
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

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.participant,
            self.channel_name
        )

    # 웹소켓이 처음에 보내는 메시지를 여기서 받는다. 그래서 receive구만
    # type은 함수 이름으로 어떤 함수로 보낼지 제어할 수 있다.
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        users = sorted([self.me, self.friend])
        query = Q(participant=','.join(users))

        message_by_user = MessageByUser() if not MessageByUser.objects.filter(query).exists() else MessageByUser.objects.get(query)
        message_by_user.participant = ','.join(users)
        message_by_user.save()

        message = Message.objects.create(
            content=text_data_json['content'],
            from_user=User.objects.get(username=self.me),
            to_user=User.objects.get(username=self.friend)
        )
        message_by_user.message.add(message)

        await self.channel_layer.group_send(
            self.participant,
            {
                'type': 'chat_message',
                'content': message.content,
                'from_user': message.from_user.username,
                'to_user': message.to_user.profile.get_name(),
                'created': message.created.strftime('%Y-%m-%d %H:%M')
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'content': event['content'],
            'from_user': event['from_user'],
            'to_user': event['to_user'],
            'created': event['created'],
        }))
