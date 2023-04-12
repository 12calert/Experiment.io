from django.db import models
from django.conf import settings
import uuid
# Create your models here.

class Researcher(models.Model):
    # all the details for each Researcher is stored in the User model, no point duplicating data
    userkey = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    researcher_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # PK

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
                fields=['name','created_by'],
                name='researcher_and_name_unique'
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
    MAPTASK = "MT"
    GAME_TYPE_CHOICES = [
        (MAPTASK, 'Map Task'),

    ]
    game_type = models.CharField(
        max_length=2,
        choices=GAME_TYPE_CHOICES,
        default=MAPTASK,
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name','experiment'],
                name='name_and_experiment_unique',
            ),
        ]
    def __str__(self):
        return self.name

class Game(models.Model):
    #game_id = models.OneToOneField(Chat, verbose_name=('game_id'), primary_key=True, on_delete=models.CASCADE, default = uuid.uuid4) # PK/FK
    game = models.UUIDField(default=uuid.uuid4, primary_key=True)
    completed = models.BooleanField(default=False)
    room_name = models.TextField(default = "", unique = True)
    users = models.IntegerField(default = 0) # this can be changed to an arrayfield of session ids
    has_condition = models.ForeignKey(Condition, on_delete=models.DO_NOTHING, null=False)
    public = models.BooleanField()
    follower_position = models.JSONField( default=dict(x = 0, y = 0 ) )
    # used to filter what rooms the user sees depending on the game they choose to play
    MAPTASK = "MT"
    rects = models.JSONField(null = True)
    path = models.JSONField(null = True)
    finishedFollowerURL = models.TextField(null = True)
    finishedGiverURL = models.TextField(null = True)
    GAME_TYPE_CHOICES = [
        (MAPTASK, 'Map Task'),

    ]
    game_type = models.CharField(
        max_length=2,
        choices=GAME_TYPE_CHOICES,
        default=MAPTASK,
    )

class Move(models.Model):
    MOVE = "mv"
    UNDO = "un"
    MOVE_TYPE_CHOICES = [
        (MOVE, 'Move'),
        (UNDO, 'Undo')
    ]
    move_type = models.CharField(max_length=2,
        choices=MOVE_TYPE_CHOICES)
    oldPos = models.JSONField(null = True)
    newPos = models.JSONField(null = True)
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, null=False)

class Chat(models.Model):
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, null = False)
    chat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # PK
    content = models.TextField(default="")
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