from django.db import models

from problematiques.models import Item
from django.contrib.auth.models import User

def get_first_name(self):
    return self.first_name + " " + self.last_name

User.add_to_class("__str__", get_first_name)

# Create your models here.

class CodeEtudiant(models.Model):
    code = models.CharField(max_length=10)
    definition = models.CharField(max_length=100)

class Student(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    comite_clinique = models.BooleanField(default=False)
    date_ref_comite_clinique = models.DateField(null=True)
    plan_intervention = models.BooleanField(default=False)
    groupe_repere = models.CharField(max_length=4)
    code = models.ForeignKey(CodeEtudiant, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['nom', 'prenom']

    def __str__(self):
        return self.nom + " - " + self.prenom + " gr." + self.groupe_repere + " ( Comité Clinique: " + str(self.comite_clinique) + " - PI: " + str(self.plan_intervention) + ")"
    
class StatusProblematique(models.Model):
    nom = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nom
    
class Problematique(models.Model):
    nom = models.ForeignKey(Item, on_delete=models.CASCADE)
    status = models.ForeignKey(StatusProblematique, on_delete=models.CASCADE)
    instigateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True)
    eleve = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    # action = models.ManyToManyField(Action, blank=True)
    
    def __str__(self):
        return self.nom.nom + " - Status - " + self.status.nom


    
class StatusAction(models.Model):
    nom = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nom

        
    
class Action(models.Model):
    createur = models.ForeignKey(User, related_name='createur_foreign_key', on_delete=models.SET_NULL, null=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True)
    status = models.ForeignKey(StatusAction, on_delete=models.SET_NULL, null=True)
    problematique = models.ForeignKey(Problematique, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.description[:50] + " *- Status -* " + self.status.nom




    

