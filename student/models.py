from django.db import models

from problematiques.models import Item
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    comite_clinique = models.BooleanField(default=False)
    date_ref_comite_clinique = models.DateField(null=True)
    plan_intervention = models.BooleanField(default=False)
    groupe_repere = models.CharField(max_length=4)
    
    class Meta:
        ordering = ['nom', 'prenom']

    
    def __str__(self):
        return self.nom + " - " + self.prenom + " gr." + self.groupe_repere + " ( Comité Clinique: " + str(self.comite_clinique) + " - PI: " + str(self.plan_intervention) + ")"
    
class StatusProblematique(models.Model):
    nom = models.CharField(max_length=50)

class Problematique(models.Model):
    eleve = models.ForeignKey(Student)
    item = models.ForeignKey(Item)
    status = models.ForeignKey(StatusProblematique)
    instigateur = models.ForeignKey(User)
    