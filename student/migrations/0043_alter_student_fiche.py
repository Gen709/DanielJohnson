# Generated by Django 4.1 on 2023-11-23 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0042_alter_student_fiche'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='fiche',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
    ]
