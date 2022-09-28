from django.db import models
from django.urls import reverse

from problematiques.models import Item
from school.models import Classification
from django.contrib.auth.models import User


def get_first_name(self):
    return self.first_name + " " + self.last_name


User.add_to_class("__str__", get_first_name)

# Create your models here.


class CodeEtudiant(models.Model):
    code = models.CharField(max_length=10)
    definition = models.CharField(max_length=250, null=True)
    
    def __str__(self):
        return self.code + " " + self.definition
    
    class Meta:
        ordering = ['definition']


class Student(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    comite_clinique = models.BooleanField(default=False)
    date_ref_comite_clinique = models.DateField(null=True)
    plan_intervention = models.BooleanField(default=False)
    groupe_repere = models.CharField(max_length=4)
    code = models.ForeignKey(CodeEtudiant, on_delete=models.SET_NULL, null=True)
    fiche = models.CharField(max_length=20, null=True)
    classification = models.ForeignKey(Classification, on_delete=models.SET_NULL, null=True)
    etat_situation = models.TextField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    lang = models.CharField(max_length=10, blank=True, null=True, default=None)
    
    class Meta:
        ordering = ['nom', 'prenom']

    def __str__(self):
        return self.nom + " - " + self.prenom + " gr." + self.groupe_repere + " ( Comité Clinique: " + str(self.comite_clinique) + " - PI: " + str(self.plan_intervention) + ")"
    
    def get_absolute_url(self):
        return reverse('student-detail', kwargs={'pk': self.pk})
    
    
class StatusProblematique(models.Model):
    nom = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nom

    
class Problematique(models.Model):
    nom = models.ForeignKey(Item, on_delete=models.CASCADE)
    status = models.ForeignKey(StatusProblematique, on_delete=models.CASCADE)
    instigateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    detail = models.TextField(null=True, blank=True)
    eleve = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    # action = models.ManyToManyField(Action, blank=True)
    
    class Meta:
        unique_together = [['nom', 'eleve']]
    
    def __str__(self):
        return self.nom.nom + " - Éleve: " + self.eleve.nom + " " + self.eleve.prenom + " - Status: " + self.status.nom


class StatusAction(models.Model):
    nom = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nom

        
class Action(models.Model):
    createur = models.ForeignKey(User, related_name='createur_foreign_key', on_delete=models.SET_NULL, null=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=300, null=True)
    detail = models.TextField(null=True, blank=True)
    status = models.ForeignKey(StatusAction, on_delete=models.SET_NULL, null=True)
    problematique = models.ForeignKey(Problematique, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = [['description', 'problematique']]
    def __str__(self):
        return self.problematique.eleve.prenom + " " + self.problematique.eleve.prenom + " " + self.description[:50] + " *- Status -* " + self.status.nom


class ActionSuggestion(models.Model):
    nom = models.CharField(max_length=250)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        ordering = ['nom']
        
        
class Grades(models.Model):
    foyer = models.CharField(max_length=4)
    no_fiche = models.CharField(max_length=15)
    nom = models.CharField(max_length=200)
    classification = models.CharField(max_length=4)
    plan = models.BooleanField(null=True, blank=True)
    difficulte = models.IntegerField(null=True, blank=True)
    age_30_sept = models.IntegerField(null=True, blank=True)
    note = models.IntegerField(null=True, blank=True)
    matiere = models.CharField(max_length=50, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.matiere + " " + str(self.note)
    
    # class Meta:
    #     unique_together = ('no_fiche', 'field2',)
    
    
# class ActionDiscussion(models):
#     action = models.ForeignKey(Action, on_delete=models.CASCADE)
#     auteur = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateField()
#     lft = models.IntegerField()
#     rgt = models.IntegerField()
#     content = models.TextField()
