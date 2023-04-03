from rest_framework import serializers
from accounts.models import Game, Chat, Condition, Experiment, Move

# if Arabella wants the moves so she can recreate the path we also add that as another serializer and link it to the GameSerializer
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["created","role","content"]

class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = ["move_type", "oldPos", "newPos"]

class GameSerializer(serializers.ModelSerializer):
    chats = ChatSerializer(read_only=True, many=True, source="chat_set")
    moves = MoveSerializer(read_only = True, many=True, source="move_set")
    class Meta:
        model = Game
        # depending on if Arabella wants the positions of the things in the game we add it here
        fields = ["completed", "room_name", "public", "game_type", "rects", "path", "moves", "chats"]

class ConditionSerializer(serializers.ModelSerializer):
    games = GameSerializer(read_only=True, many=True, source="game_set")
    class Meta:
        model=Condition
        fields=["name","amount_item", "restriction","active", "games"]

class ExperimentSerializer(serializers.ModelSerializer):
    conditions = ConditionSerializer(read_only=True, many=True, source="condition_set")
    class Meta:
        model=Experiment
        fields=["name","active","conditions"]