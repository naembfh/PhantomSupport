import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from sockets.models import Message, Room
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        # Add the channel to the group
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the channel from the group
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        timestamp = datetime.now().isoformat() 

        # Broadcast message to the group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'timestamp': timestamp,
            }
        )

    async def chat_message(self, event):
        # Get the message data from the event
        message_data = {
            'sender': event['sender'],
            'message': event['message'],
            'timestamp': event['timestamp'],
        }
        
        # Save the message to the database
        await self.create_message(message_data)

        # Send the message back to WebSocket
        await self.send(text_data=json.dumps({'message': message_data}))

    @database_sync_to_async
    def create_message(self, data):
        room = Room.objects.get(room_name=self.scope['url_route']['kwargs']['room_name'])
        Message.objects.create(room=room, sender=data['sender'], message=data['message'])
