# Generated by Django 4.1 on 2023-09-19 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0034_student_created_by_student_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problematique',
            name='eleve',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.student'),
        ),
    ]
