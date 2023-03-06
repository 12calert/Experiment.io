# adapted from https://channels.readthedocs.io/en/stable/tutorial/part_3.html
import json

from asgiref.sync import sync_to_async
from accounts.models import Game, Chat
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        self.room = await Game.objects.aget(room_name=self.room_name)    
        
        self.room.users += 1
        await sync_to_async(self.room.save)()
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

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
        if (not finished):
            # NOTE: this creates two entries in the database since there are two websocket connections, this needs to be made using ajax in game_view.html
            await Chat.objects.acreate(game = self.room, content = message, role = role)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "role": role, "finished":finished}))