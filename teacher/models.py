from django.db import models
from django.contrib.auth.models import User
from school.models import Group
from itertools import chain


# Create your models here.
class SchoolAdmin(User):
    resp = models.IntegerField(default=None, null=True, blank=True)

    @property
    def get_teacher(self):
        group = [[g.regularteacher for g in classification.group_set.all()] for classification in self.classification_set.all() if classification.group_set.all()]

        group = flattened_list = list(chain(*group))

        return group

    class Meta:
        verbose_name = 'Administrateur'
        verbose_name_plural = 'Administrateurs'

class RegularTeacher(User):
    group = models.OneToOneField(Group, on_delete=models.SET_NULL, null=True)
    matière = models.CharField(max_length=30, blank=True, null=True)
    local =  models.CharField(max_length=30, blank=True, null=True, default=None)
    
    @property
    def responsible_children(self):
        if self.group:
            return self.group.student_set.all()
        return []
    
    def delete(self, *args, **kwargs):
            # Delete the associated user
            self.user.delete()
            # Call the parent class's delete method to delete the subclass instance
            super().delete(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()  
    
    class Meta:
        verbose_name = 'Enseignant Généraliste'
        verbose_name_plural = 'Enseignants Généralistes'


class SpecialtyTeacher(User):
    all_groups = models.ManyToManyField(Group)
    matière = models.CharField(max_length=30, blank=True, null=True)
    local =  models.CharField(max_length=30, blank=True, null=True, default=None)

    def delete(self, *args, **kwargs):
            # Delete the associated user
            self.user.delete()
            # Call the parent class's delete method to delete the subclass instance
            super().delete(*args, **kwargs)

    def __str__(self):
        return self.get_full_name() + " " + self.matière
    
    class Meta:
        verbose_name = 'Enseignant Spécialisé'
        verbose_name_plural = 'Enseignants Spécialisés'

   
class Professional(User):
    speciality = models.CharField(max_length=100, blank=True, null=True, default=None)
    local =  models.CharField(max_length=30, blank=True, null=True, default=None)

    def delete(self, *args, **kwargs):
            # Delete the associated user
            self.user.delete()
            # Call the parent class's delete method to delete the subclass instance
            super().delete(*args, **kwargs)

    def __str__(self):
        return self.get_full_name() + " (" + self.speciality + ")"

    class Meta:
            verbose_name = 'Professionel'
            verbose_name_plural = 'Professionels'
    