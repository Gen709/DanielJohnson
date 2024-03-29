from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class CategorieEmplois(models.Model):
    code = models.CharField(max_length=5)
    description = models.CharField(max_length=100, null=True, default=None)
    def __str__(self):
        return self.description

class Emplois(models.Model):
    categorie_emplois = models.ForeignKey(CategorieEmplois, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=5)
    description = models.CharField(max_length=100, null=True, default=None)

    def __str__(self):
        return self.description

class Classification(models.Model):
    nom = models.CharField(max_length=5)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return "Nom: " + self.nom + " - Resp: " + str(self.owner)
    
class Local(models.Model):
    nom = models.CharField(max_length=15, unique=True)
    capacity = models.SmallIntegerField(null=True, blank=True)

class Matiere(models.Model):
    school_code = models.CharField(max_length=6)
    subject_code = models.CharField(max_length=8)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=50, null=True, default=None)
    visible_to_parents = models.BooleanField()
    mat_2nd = models.CharField(max_length=7, null=True, default=None)
    est_enseigne = models.BooleanField(default=False)
    matiere_de_base = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject_code} - {self.description}"
    class Meta:
        ordering = ['est_enseigne', 'subject_code']
    
class Competence(models.Model):
    nom = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.nom}"
    class Meta:
        ordering = ['nom']

class CompetencesEvaluees(models.Model):
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.matiere.subject_code} - {self.matiere.description} - {self.competence.nom}"
    class Meta:
        ordering = ['matiere__subject_code', "competence__nom"]

class Group(models.Model):
    # TODO: Ajouter établissement le temps venu
    nom = models.CharField(max_length=10, unique=True)
    classification = models.ForeignKey(Classification, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.classification:
            b = self.classification.nom
        else:
            b="Unknown"
        return "Nom: " + self.nom + ' Classification: ' + b