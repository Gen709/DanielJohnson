# Generated by Django 4.1 on 2023-09-29 23:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0037_remove_student_classification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='groupe_repere',
        ),
    ]