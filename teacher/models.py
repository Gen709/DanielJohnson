from django.db import models
from django.contrib.auth.models import User
from school.models import Group


# Create your models here.
class SchoolAdmin(User):
    resp = models.IntegerField(default=None, null=True, blank=True)


class RegularTeacher(User):
    group = models.OneToOneField(Group, on_delete=models.SET_NULL, null=True)
    matière = models.CharField(max_length=30, blank=True, null=True)
    local =  models.CharField(max_length=30, blank=True, null=True, default=None)
    
    @property
    def responsible_children(self):
        if self.group:
            return self.group.student_set.all()
        return []
   
    def __str__(self):
        return self.first_name + " " + self.last_name 


class SpecialtyTeacher(User):
    all_groups = models.ManyToManyField(Group)
    matière = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

   
class Professional(User):
    speciality = models.CharField(max_length=100, blank=True, null=True, default=None)
    local =  models.CharField(max_length=30, blank=True, null=True, default=None)
    