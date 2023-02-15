from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
     
INSTALLED_APPS = [
    'researcher.apps.ContactConfig' ]

INSTALLED_APPS = [
    'researcher.apps.ContactConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]