from django.db import models

# Create your models here.

class Categorie(models.Model):
    nom = models.CharField(max_length=200)
    
class Item(models.Model):
    nom = models.CharField(max_length=200)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)