import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth import get_user_model
from .models import Message
from .serializers import MessageSerializer

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = None
        
        self.scope['user'] = None
        
        try:
            jwt_token = self.scope['query_string'].decode().split('=')[-1]
            access_token = AccessToken(jwt_token)
            user_id = access_token.payload.get('user_id')
            if user_id:
                user = await database_sync_to_async(User.objects.get)(id=user_id)
                self.user = user
                self.scope['user'] = user
                
                self.room_name = f"chat_room"
                self.room_group_name = f'chat_{self.room_name}'
            else:
                await self.close()
        except Exception as e:
            print(e)
            await self.close()

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

    async def create_message_with_file(self, sender, receiver, message, uploaded_file):
        message_obj = await database_sync_to_async(Message.objects.create)(
            sender=sender,
            receiver=receiver,
            message=message,
            file=uploaded_file
        )
        return message_obj

    async def create_message(self, sender, receiver, message):
        message_obj = await database_sync_to_async(Message.objects.create)(
            sender=sender,
            receiver=receiver,
            message=message
        )
        return message_obj

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')
            recipient_id = text_data_json.get('recipient_id')
            file = text_data_json.get('file')
            
            sender = self.scope['user']
            recipient = await database_sync_to_async(User.objects.get)(pk=recipient_id)

            if file:
                file_data = BytesIO(file['data'])
                file_data.seek(0)
                file_name = file['name']
                file_content_type = file['content_type']
                file_size = file['size']

                uploaded_file = InMemoryUploadedFile(
                    file_data,
                    field_name='file',
                    name=file_name,
                    content_type=file_content_type,
                    size=file_size,
                    charset='utf-8'
                )

                message_obj = await self.create_message_with_file(sender, recipient, message, uploaded_file)
            else:
                message_obj = await self.create_message(sender, recipient, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': MessageSerializer(message_obj).data
                }
            )
        except Exception as e:
            print(f'Error: {str(e)}')

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def read_receipt(self, event):
        message_id = event['message_id']
        receiver = event['receiver']

        message = await database_sync_to_async(Message.objects.get)(id=message_id)
        message.read_receipt = True
        await database_sync_to_async(message.save)()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_read_receipt',
                'message_id': message_id,
                'receiver': receiver
            }
        )

    async def send_read_receipt(self, event):
        message_id = event['message_id']
        receiver = event['receiver']

        await self.send(text_data=json.dumps({
            'message_id': message_id,
            'receiver': receiver,
            'read_receipt': True
        }))
