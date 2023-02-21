from django.db import models
from django.conf import settings
from jsonfield import JSONField
import uuid
from django.contrib.auth.models import User
# Create your models here.

class Researcher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # userkey = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="") # FK UNCOMMENT LATER, IT IS COMMENTED OUT ONLY INITALLY
    researcher_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # PK
    
    name = models.TextField()
    surname = models.TextField()
    email = JSONField()
    username = models.TextField(default="")
    password = models.TextField()
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

class Condition(models.Model):
    condition_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    amount_item = models.IntegerField()
    restriction = models.TextField()
    active = models.BooleanField(default = True)
