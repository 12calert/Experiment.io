# chat/routing.py
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/all_rooms/game_view/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]