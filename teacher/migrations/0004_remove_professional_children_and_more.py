# Generated by Django 4.1 on 2023-10-02 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_schooladmin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professional',
            name='children',
        ),
        migrations.RemoveField(
            model_name='professional',
            name='name',
        ),
    ]
