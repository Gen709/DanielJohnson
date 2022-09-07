from django.db import models

# Create your models here.

class Classification(models.Model):
    nom = models.CharField(max_length=5)