# Generated by Django 4.1.3 on 2023-02-14 22:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_chat_researcher_game_delete_customuser"),
    ]

    operations = [
        migrations.AddField(
            model_name="researcher",
            name="password",
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
