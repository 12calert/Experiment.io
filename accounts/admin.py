from django.contrib import admin
from accounts.models import Researcher, Game
from django.db import models
from django.conf import settings
from jsonfield import JSONField
import uuid
from django.contrib.auth.models import User
class AuthorAdmin(admin.ModelAdmin):
    
    pass
# Add this if you want to view the Games online in admin
# admin.site.register(Game)

admin.site.register(Researcher, AuthorAdmin)
