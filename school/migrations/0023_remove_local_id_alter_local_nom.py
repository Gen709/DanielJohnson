# Generated by Django 4.1 on 2024-08-21 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0022_alter_competence_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='local',
            name='id',
        ),
        migrations.AlterField(
            model_name='local',
            name='nom',
            field=models.CharField(max_length=15, primary_key=True, serialize=False, unique=True),
        ),
    ]
