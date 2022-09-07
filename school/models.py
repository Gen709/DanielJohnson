from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Classification(models.Model):
    nom = models.CharField(max_length=5)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.nom