import json

from channels.generic.websocket import WebsocketConsumer

""" consumer which serves the chat users """
class ChatConsumer(WebsocketConsumer):
    """ accpets all connections"""
    def connect(self):
        self.accept()
    
    """ do something on disconnect """
    def disconnect(self, close_code):
        pass

    """ receives text messages from chat and sends to itself"""
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))