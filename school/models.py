from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Classification(models.Model):
    nom = models.CharField(max_length=5)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.nom + " - Resp: " + str(self.owner)
    
class Local(models.Model):
    nom = models.CharField(max_length=15, unique=True)
    capacity = models.SmallIntegerField(null=True, blank=True)

# class LocalAttribution(models.Model):
#     school_year = models.CharField(max_length=10)
#     week_day = models.SmallIntegerField(null=True, blank=True)
#     start_period = models.TimeField(null=True, blank=True)
#     end_period = models.TimeField(null=True, blank=True)
#     # subject + group -> teacher 

# class subject(models.Model):
#     code = models.CharField(max_length=10)
#     name = models.CharField(max_length=100)
#     classification = models.ForeignKey(Classification, on_delete=models.SET_NULL)

class Group(models.Model):
    nom = models.CharField(max_length=10, unique=True)
    classification = models.ForeignKey(Classification, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.classification:
            b = self.classification.nom
        else:
            b="Unknown"
        return self.nom + ' ' + b