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

class Experiment(models.Model):
    experiment_id = models.UUIDField(default = uuid.uuid4, primary_key = True)
    name = models.TextField(null = False)
    created_by = models.ForeignKey(Researcher, on_delete = models.DO_NOTHING, null = False)

class Condition(models.Model):
    condition_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    amount_item = models.IntegerField()
    restriction = models.TextField(null=True)
    active = models.BooleanField(default = True)
    created_by = models.ForeignKey(Researcher, on_delete=models.DO_NOTHING, null=False)
    name = models.TextField(default = "name not set", null = False)
    experiment = models.ForeignKey(Experiment, on_delete = models.DO_NOTHING, null = True)
    MAPGAME = "MG"
    GAME_TYPE_CHOICES = [
        (MAPGAME, 'Map Game'),

    ]
    game_type = models.CharField(
        max_length=2,
        choices=GAME_TYPE_CHOICES,
        default=MAPGAME,
    )

class Game(models.Model):
    game_id = models.OneToOneField(Chat, verbose_name=('game_id'), primary_key=True, on_delete=models.CASCADE, default = uuid.uuid4) # PK/FK
    final_map = models.TextField(default="")
    completed = models.BooleanField(default=False)
    room_name = models.TextField(default = "")
    users = models.IntegerField(default = 0) # this can be changed to an arrayfield of session ids
    has_condition = models.ForeignKey(Condition, on_delete=models.DO_NOTHING, null=False)
    public_yes_or_no = models.BooleanField()
    # used to filter what rooms the user sees depending on the game they choose to play
    MAPGAME = "MG"
    GAME_TYPE_CHOICES = [
        (MAPGAME, 'Map Game'),

    ]
    game_type = models.CharField(
        max_length=2,
        choices=GAME_TYPE_CHOICES,
        default=MAPGAME,
    )

class Player(models.Model):
    FOLLOWER = "follower"
    GIVER = "giver"
    ROLE_CHOICES = [
        (FOLLOWER, "Follower"),
        (GIVER, "Giver")
    ]
    role = models.CharField(
        max_length=8,
        choices=ROLE_CHOICES
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null = False)
    user_session = models.CharField(max_length = 10, null = False)