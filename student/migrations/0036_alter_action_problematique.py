# Generated by Django 4.1 on 2023-09-25 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0035_alter_problematique_eleve'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='problematique',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.problematique'),
        ),
    ]
