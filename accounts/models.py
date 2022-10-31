from django.db import models
from django.conf import settings
from jsonfield import JSONField

# Create your models here.

class CustomUser(models.Model):

    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    user_id = models.TextField()
    email = JSONField()
    name = models.TextField()
    surname = models.TextField()
