from django.db import models
from django.contrib.auth.models import User
from school.models import Group
from student.models import Student

# Create your models here.

class RegularTeacher(User):
    group = models.OneToOneField(Group, on_delete=models.SET_NULL, null=True)
    matière = models.CharField(max_length=30, blank=True, null=True)
   
    def __str__(self):
        return self.first_name

class SpecialtyTeacher(User):
    all_groups = models.ManyToManyField(Group)
    matière = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Professional(User):
    speciality = models.CharField(max_length=100, blank=True, null=True, default=None)
    name = models.CharField(max_length=100)
    children = models.ManyToManyField(Student)

    def __str__(self):
        return self.name