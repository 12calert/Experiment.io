# Generated by Django 4.1.6 on 2023-02-07 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('game_id', models.UUIDField(default=uuid.uuid4)),
                ('chat_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('researcher_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', jsonfield.fields.JSONField()),
                ('name', models.TextField()),
                ('surname', models.TextField()),
                ('approved', models.BooleanField(default=False)),
                ('userkey', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('game_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.chat', verbose_name='game_id')),
                ('final_map', models.TextField(default='')),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]