# Generated by Django 4.1.3 on 2023-02-22 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0010_alter_game_private_no_or_yes"),
    ]

    operations = [
        migrations.RenameField(
            model_name="game",
            old_name="private_no_or_yes",
            new_name="public_yes_or_no",
        ),
    ]