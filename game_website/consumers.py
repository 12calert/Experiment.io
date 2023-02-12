# adapted from https://channels.readthedocs.io/en/stable/tutorial/part_3.html
import json

from asgiref.sync import sync_to_async
from accounts.models import Room
from channels.generic.websocket import AsyncWebsocketConsumer

""" currently synchronous, to be made asynchronous later """
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        # try to enter the room that already has been created
        try:
            self.room = await Room.objects.aget(room_name=self.room_name)
    
        # this is the case in which the room does not exist
        except Room.DoesNotExist:
            self.room = await Room.objects.acreate(room_name=self.room_name, connected_user=1)
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            await self.accept()
            return
        
        if self.room.connected_user >= 2:
            # shouldn't be needed here since we route them to a correct room automatically, 
            # this will stop from someone joining the room and talking directly via URL
            return self.close()
        else:
            self.room.connected_user += 1
            await sync_to_async(self.room.save)()
            # Join room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        self.room.connected_user -= 1
        await sync_to_async(self.room.save)()
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, {"type": "chat_message", "message": message})

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))