import asyncio, json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.core import serializers

from users.models import User
from lessons.models import Lesson
from chat_ws.models import Msg


class ChatConsumer(AsyncConsumer):
    chat_room = None
    users = []
    lessons = []

    async def websocket_connect(self, _):
        await self.send({
            'type': 'websocket.accept'
        })

        if not self.users:
            self.users = json.dumps(await self.get_users(), ensure_ascii=False, separators=(',', ': '))
            print('Пользователи', self.users)
        if not self.lessons:
            self.lessons = json.dumps(await self.get_lessons(), ensure_ascii=False, separators=(',', ': '))
            print('Предметы', self.lessons)

        data = {
            "status": 'init-data',
            "users": self.users,
            "lessons": self.lessons
        }

        await self.send({
            'type': 'websocket.send',
            'text': json.dumps(data, ensure_ascii=False)
        })

    async def websocket_receive(self, event):
        front_data = event.get('text', None)
        if front_data is not None:
            data = json.loads(front_data)


            if data['type'] == 'customization':
                print('Настройка чата')
                self.chat_room = json.dumps(data['lesson'], ensure_ascii=True)

                messages = json.dumps(await self.get_messages(data['lesson']), ensure_ascii=False,
                                      separators=(',', ': '))

                data = {
                    "status": 'init-messages',
                    "messages": messages
                }

                await self.channel_layer.group_add(
                    self.chat_room,
                    self.channel_name
                )

                await self.send({
                    'type': 'websocket.send',
                    'text': json.dumps(data, ensure_ascii=False)
                })

            elif data['type'] == 'chat':
                response = json.dumps(
                    {'status': 'chat', 'text': data['message'], 'lesson': data['lesson'], 'user': data['user']},
                    ensure_ascii=False, separators=(',', ': '))

                # сохраняем сообщение в базу
                await self.save_msg(data['message'], data['lesson'], data['user'])

                await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        'type': 'chat_message',
                        'text': response
                    }
                )

    async def chat_message(self, event):
        print(('message', event))
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def websocket_disconnect(self, event):
        print("disconnected ", event)

    def serialize_with_id(self, json_data):
        arr = []
        for i in json.loads(json_data):
            i['fields']['id'] = i['pk']
            arr.append(i['fields'])
        return arr
    @database_sync_to_async
    def get_users(self):
        try:
            json_data = serializers.serialize("json", User.objects.all(), fields=('id', 'f_name', 'type', 'access'))
            return self.serialize_with_id(json_data)
        except:
            print('get_users: something went wrong...')

    @database_sync_to_async
    def get_lessons(self):
        try:
            json_data = serializers.serialize("json", Lesson.objects.all())
            return self.serialize_with_id(json_data)
        except:
            print('get_lessons: something went wrong...')

    @database_sync_to_async
    def save_msg(self, message, lesson, owner):
        try:
            new_msg = Msg.objects.create(text=message, lesson_id=lesson, owner_id=owner)
            new_msg.save()
        except:
            print('save_msg: something went wrong...')

    @database_sync_to_async
    def get_messages(self, lesson):
        try:
            json_data = serializers.serialize("json", Msg.objects.filter(lesson=lesson))
            return self.serialize_with_id(json_data)
        except:
            print('get_messages: something went wrong...')
