# Generated by Django 4.1 on 2022-08-23 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0014_problematique_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problematique',
            name='description',
        ),
    ]
