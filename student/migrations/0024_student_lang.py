# Generated by Django 4.1 on 2022-09-02 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0023_alter_actionsuggestion_options_student_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='lang',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
    ]
