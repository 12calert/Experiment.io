# Generated by Django 4.1.7 on 2023-03-10 16:21

from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_condition_name_alter_experiment_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condition',
            name='name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='name',
            field=models.TextField(),
        ),
        migrations.AddConstraint(
            model_name='condition',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), models.F('experiment'), name='name_and_experiment_unique'),
        ),
        migrations.AddConstraint(
            model_name='experiment',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), models.F('created_by'), name='researcher_and_name_unique'),
        ),
    ]
