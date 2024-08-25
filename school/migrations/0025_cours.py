# Generated by Django 4.1 on 2024-08-21 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0024_rename_nom_local_local_local_champ_01_local_champ_02_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cours',
            fields=[
                ('Cours', models.CharField(max_length=6, primary_key=True, serialize=False, unique=True)),
                ('Description', models.CharField(blank=True, max_length=250, null=True)),
                ('Grille', models.CharField(blank=True, max_length=25, null=True)),
                ('Type', models.CharField(blank=True, max_length=10, null=True)),
                ('Grp_prév', models.CharField(blank=True, max_length=25, null=True)),
            ],
        ),
    ]
