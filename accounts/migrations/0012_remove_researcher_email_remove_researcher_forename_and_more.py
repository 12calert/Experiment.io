# Generated by Django 4.1.7 on 2023-03-10 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_remove_researcher_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='researcher',
            name='email',
        ),
        migrations.RemoveField(
            model_name='researcher',
            name='forename',
        ),
        migrations.RemoveField(
            model_name='researcher',
            name='password',
        ),
        migrations.RemoveField(
            model_name='researcher',
            name='surname',
        ),
        migrations.RemoveField(
            model_name='researcher',
            name='username',
        ),
    ]