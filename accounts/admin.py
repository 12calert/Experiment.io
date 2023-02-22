from django.contrib import admin
from accounts.models import Researcher

class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Researcher, AuthorAdmin)
