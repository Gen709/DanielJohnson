from django.db import models

from student.models import Student

# Create your models here.

class Categorie(models.Model):
    nom = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nom
    
class Item(models.Model):
    nom = models.CharField(max_length=200)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    student = models.ManyToManyField(Student)
    
    def __str__(self):
        return self.nom +" (" + self.categorie.nom + ")"