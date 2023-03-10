from django.db import models
from django.conf import settings
import uuid
from django.db.models.functions import Lower
# Create your models here.

class Researcher(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    userkey = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    researcher_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # PK
    
    forename = models.CharField(max_length=50, null = False)
    surname = models.CharField(max_length=50, null = False)
    email = models.EmailField(max_length = 254, null = False)
    username = models.TextField(null = False, unique = True)
    password = models.CharField(max_length=50, null = False)

    # removes the need to store this as a field now we just call this
    def is_approved(self):
        return self.userkey.is_active if self.userkey else None


class Experiment(models.Model):
    experiment_id = models.UUIDField(default = uuid.uuid4, primary_key = True)
    name = models.TextField(null = False)
    created_by = models.ForeignKey(Researcher, on_delete = models.DO_NOTHING, null = False)
    active = models.BooleanField(default = True)

    class Meta:
        # ensure Researcher's set a unique name for their experiment
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                'created_by',
                name='researcher_and_name_unique',
            ),
        ]

    def __str__(self):
        return self.name

class Condition(models.Model):
    condition_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    amount_item = models.IntegerField()
    restriction = models.TextField(null=True)
    active = models.BooleanField(default = True)
    created_by = models.ForeignKey(Researcher, on_delete=models.DO_NOTHING, null=False)
    name = models.TextField(null = False)
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
    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                'experiment',
                name='name_and_experiment_unique',
            ),
        ]
    
    def __str__(self):
        return self.name

class Game(models.Model):
    #game_id = models.OneToOneField(Chat, verbose_name=('game_id'), primary_key=True, on_delete=models.CASCADE, default = uuid.uuid4) # PK/FK
    game = models.UUIDField(default=uuid.uuid4, primary_key=True)
    final_map = models.TextField(default="")
    completed = models.BooleanField(default=False)
    room_name = models.TextField(default = "", unique = True)
    users = models.IntegerField(default = 0) # this can be changed to an arrayfield of session ids
    has_condition = models.ForeignKey(Condition, on_delete=models.DO_NOTHING, null=False)
    public = models.BooleanField()
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

class Chat(models.Model):
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, null = False)
    chat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # PK
    content = models.TextField(default="") # {"0": {"origin": leader/follower, "msg": msg, "timestamp": date}}
    role = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True, editable=False)

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