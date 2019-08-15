from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.contrib.auth.models import User
from django.db.models import Q

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

        self.__member_list.append(self.me)
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
        self.__channels_list[self.participant].remove(self.me)

    # 웹소켓이 처음에 보내는 메시지를 여기서 받는다. 그래서 receive구만
    # type은 함수 이름으로 어떤 함수로 보낼지 제어할 수 있다.
    async def receive(self, text_data):
        left = len(self.__channels_list[self.participant]) == 1
        print(left)
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

        query = Q(user=user) & Q(friend=friend)
        message_box = MessageBox.objects.get(query) if MessageBox.objects.filter(query).exists() else MessageBox.objects.create(user=user, friend=friend)
        message_box.message.add(message)

        query2 = Q(user=friend) & Q(friend=user)
        message_box2 = MessageBox.objects.get(query2) if MessageBox.objects.filter(query2).exists() else MessageBox.objects.create(user=friend, friend=user)
        message_box2.message.add(message)

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