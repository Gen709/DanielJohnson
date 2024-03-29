# Generated by Django 4.1 on 2023-09-29 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0037_remove_student_classification'),
        ('teacher', '0002_professional_regularteacher_specialtyteacher_and_more'),
        ('school', '0009_remove_group_regular_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='regular_teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups_regular', to='teacher.regularteacher'),
        ),
        migrations.AddField(
            model_name='group',
            name='students',
            field=models.ManyToManyField(to='student.student'),
        ),
    ]
