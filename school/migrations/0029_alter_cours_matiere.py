# Generated by Django 4.1 on 2024-08-22 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0028_attribute_classroomattribute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cours',
            name='matiere',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]