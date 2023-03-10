# Generated by Django 4.1.7 on 2023-03-10 18:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0009_alter_condition_name_alter_experiment_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='researcher',
            name='user',
        ),
        migrations.AddField(
            model_name='researcher',
            name='userkey',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
