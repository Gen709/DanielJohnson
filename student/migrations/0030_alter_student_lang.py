# Generated by Django 4.1 on 2022-10-09 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0029_alter_action_options_alter_student_fiche_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='lang',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]
