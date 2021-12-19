import asyncio, json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from users.models import User


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        users = await self.get_users()
        print(users)
        await self.send({
            'type': "websocket.accept"
        })
        # await asyncio.sleep(10)
        chat_room = f'lesson_id'
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        await self.send({
            'type': "websocket.send",
            'text': 'WS working!!!!'
        })

    async def websocket_receive(self, event):
        print("receive", event)
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            print(loaded_dict_data['message'])
            response = json.dumps({"code": 200, "response": loaded_dict_data['message']})
            new_event = {
                'type': "websocket.send",
                'text': response
            }
            await self.channel_layer.group_send(
                self.chat_room,
                new_event
            )
            # await self.send()

    async def websocket_disconnect(self, event):
        print("disconnected ", event)

    @database_sync_to_async
    def get_users(self):
        return User.objects.get(email='vasya@mail.ru').email


