from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'chat_room'
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        sender = text_data_json.get('sender')
        recipient_id = text_data_json.get('recipient_id')
        message_file = text_data_json.get('message_file')
        image = text_data_json.get('image')
        text = text_data_json.get('text')
        audio = text_data_json.get('audio')

        recipient = User.objects.get(pk = recipient_id)
        # Save the message to the database
        Message.objects.create(sender=sender, recipient=recipient, message_file=message_file, image=image, text=text, audio=audio)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
