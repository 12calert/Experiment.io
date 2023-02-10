# adapted from https://channels.readthedocs.io/en/stable/tutorial/part_3.html
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from accounts.models import Room

""" currently synchronous, to be made asynchronous later """
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        try:
            self.room = Room.objects.get(room_name=self.room_name)
        
        # this is the case in which the room does not exist
        except Room.DoesNotExist:
            self.room = Room.objects.create(room_name=self.room_name, connected_user=1)
            self.room.save(update_fields=['connected_user'])
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )

            self.accept()
            return
        
        if self.room.connected_user >= 2:
            print(self.room.connected_user)
            return self.close()
        else:
            self.room.connected_user += 1
            self.room.save(update_fields=['connected_user'])
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )

            self.accept()

    def disconnect(self, close_code):
        # Leave room group
        self.room.connected_user -= 1
        self.room.save(update_fields=['connected_user'])
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))