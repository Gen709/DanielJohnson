# Generated by Django 4.1 on 2022-08-23 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0017_alter_action_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='detail',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='problematique',
            name='detail',
            field=models.TextField(blank=True, null=True),
        ),
    ]