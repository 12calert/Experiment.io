# Generated by Django 4.1.7 on 2023-02-20 19:19

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            name='Condition',
            fields=[
                ('condition_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('amount_item', models.IntegerField()),
                ('restriction', models.TextField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('researcher_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('surname', models.TextField()),
                ('email', jsonfield.fields.JSONField()),
                ('password', models.TextField()),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('game_id', models.OneToOneField(default=uuid.uuid4, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.chat', verbose_name='game_id')),
                ('final_map', models.TextField(default='')),
                ('completed', models.BooleanField(default=False)),
                ('room_name', models.TextField(default='')),
                ('users', models.IntegerField(default=0)),
            ],
        ),
    ]
