from django.db import models
from django.conf import settings
from jsonfield import JSONField
import uuid

# Create your models here.

class Researcher(models.Model):

    userkey = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="") # FK
    researcher_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # PK
    email = JSONField()
    name = models.TextField()
    surname = models.TextField()
    approved = models.BooleanField(default=False)

class Chat(models.Model):
    game_id = models.UUIDField(default=uuid.uuid4) # FK
    chat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # PK
    content = models.TextField(default="") # {"0": {"origin": leader/follower, "msg": msg, "timestamp": date}}

class Game(models.Model):
    game_id = models.OneToOneField(Chat, verbose_name=('game_id'), primary_key=True, on_delete=models.CASCADE, default = uuid.uuid4) # PK/FK
    final_map = models.TextField(default="")
    completed = models.BooleanField(default=False)
    room_name = models.TextField(default = "")
    users = models.IntegerField(default = 0) # this can be changed to an arrayfield of session ids

