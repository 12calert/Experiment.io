# adapted from https://channels.readthedocs.io/en/stable/tutorial/part_3.html
import json

from asgiref.sync import sync_to_async
from accounts.models import Game, Chat
from channels.generic.websocket import AsyncWebsocketConsumer

# this whole file needs refactoring
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        self.room = await Game.objects.aget(room_name=self.room_name)    
        
        self.room.users += 1
        await sync_to_async(self.room.save)()
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.channel_layer.group_send(self.room_group_name, {"type": "announcement", "message": "A user has connected!" , "finished":False})

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        self.room.users -= 1
        await sync_to_async(self.room.save)()
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        role = text_data_json["role"]
        finished = text_data_json["finished"]

        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, {"type": "chat_message", "message": message, "role": role, "finished":finished})

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        role = event["role"]
        finished = event["finished"]
        # after sending a message create entry in DB and connect it to the specific game
        if role != "announcement":
            # Send message to WebSocket
            await self.send(text_data=json.dumps({"type": "chat_message", "message": message, "role": role, "finished":finished}))
        else:
            await self.send(text_data=json.dumps({"type":"announcement", "message":message, "finished":False}))
    
    async def announcement(self,event):
        message = event["message"]
        finished = event["finished"]

        await self.send(text_data=json.dumps({"type":"announcement", "message":message, "finished":finished}))