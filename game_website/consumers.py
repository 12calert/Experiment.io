# adapted from https://channels.readthedocs.io/en/stable/tutorial/part_3.html
import json

from asgiref.sync import sync_to_async
from accounts.models import Game
from channels.generic.websocket import AsyncWebsocketConsumer

# this whole file needs refactoring
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        self.room = await Game.objects.aget(room_name=self.room_name)    
        if self.room.users == 0:
            #intialise the game...
            pass
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

        if role == "move":
            game = await Game.objects.aget( room_name=self.room_name )
            game.follower_position[ "x" ] += message[ "x" ] * 10
            game.follower_position[ "y" ] += message[ "y" ] * 10
            await sync_to_async( game.save )()
            #game.follower_position[ "rects" ] = game.rects
            message = game.follower_position
            self.channel_layer.group_send(self.room_group_name, {"type": "move", "message": message, "finished":False})
        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, {"type": "chat_message", "message": message, "role": role, "finished":finished})

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        role = event["role"]
        finished = event["finished"]
        # after sending a message create entry in DB and connect it to the specific game
        if role == "announcement":
            await self.send(text_data=json.dumps({"type":"announcement", "message":message, "finished":False}))
        elif role == "move":
            await self.send(text_data=json.dumps( { "type":"move", "message":message, } ) )
        else:
            # Send message to WebSocket
            await self.send(text_data=json.dumps({"type": "chat_message", "message": message, "role": role, "finished":finished}))
    
    async def announcement(self,event):
        message = event["message"]
        finished = event["finished"]

        await self.send(text_data=json.dumps({"type":"announcement", "message":message, "finished":finished}))
    
    async def move( self, event ):
        message = event[ "message" ]

        await self.send( text_data=json.dumps( { "type":"move", "message":message, "finished":False } ) )