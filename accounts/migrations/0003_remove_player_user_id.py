# Generated by Django 4.1.7 on 2023-02-26 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_player'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='user_id',
        ),
    ]
