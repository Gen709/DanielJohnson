# Generated by Django 4.1 on 2022-09-02 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0022_actionsuggestion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actionsuggestion',
            options={'ordering': ['nom']},
        ),
        migrations.AddField(
            model_name='student',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]