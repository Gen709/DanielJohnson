# Generated by Django 4.1 on 2023-10-02 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0012_remove_group_students'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='regular_teacher',
        ),
    ]
