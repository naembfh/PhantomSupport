
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Log WebSocket connection in the console
        print("WebSocket connected")
        
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Log WebSocket disconnection in the console
        print(f"WebSocket disconnected with code {close_code}")
        pass

    async def receive(self, text_data):
        # Log received data in the console
        print(f"Received data: {text_data}")
        
        # Send a response back to the WebSocket
        await self.send(text_data=json.dumps({
            'message': 'Message received!'
        }))
