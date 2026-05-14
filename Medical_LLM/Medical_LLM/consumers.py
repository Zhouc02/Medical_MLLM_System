# consumers.py

import json
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer

from Medical_LLM.settings import mysql_pool


class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        from_id = text_data_json['from_id']
        to_id = text_data_json['to_id']

        message = text_data_json['content']

        # Send message to room group

        now = datetime.now()
        add_time = now.strftime("%Y年%m月%d日%H:%M")
        connection = mysql_pool.connection()
        with connection.cursor() as cursor:
            result = cursor.execute(
                "insert into feedback values ({},{},'{}','{}');".format(int(from_id), int(to_id), message,
                                                                        add_time))
            connection.commit()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        #
        # await self.send(text_data=json.dumps({
        #     'message': message
        # }))

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


class DoctorsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'doctors'
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        from_id = text_data_json['from_id']
        message = text_data_json['content']

        # Send message to room group
        connection = mysql_pool.connection()

        now = datetime.now()
        add_time = now.strftime("%Y年%m月%d日%H:%M")
        with connection.cursor() as cursor:
            result = cursor.execute(
                "insert into doctor_help values ({},'{}','{}');".format(int(from_id), message, add_time))
            connection.commit()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        #
        # await self.send(text_data=json.dumps({
        #     'message': message
        # }))

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
