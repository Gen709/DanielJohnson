# Generated by Django 4.1 on 2022-08-23 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0018_alter_action_detail_alter_problematique_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codeetudiant',
            name='definition',
            field=models.CharField(max_length=250, null=True),
        ),
    ]