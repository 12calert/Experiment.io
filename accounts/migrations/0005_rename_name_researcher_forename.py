# Generated by Django 4.1.3 on 2023-03-06 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_add_forename_to_researcher"),
    ]

    operations = [
        migrations.RenameField(
            model_name="researcher", old_name="name", new_name="forename",
        ),
    ]