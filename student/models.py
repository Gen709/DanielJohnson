from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone


from problematiques.models import Item
from django.contrib.auth.models import User

from datetime import date, datetime

from django.shortcuts import get_object_or_404
from teacher.models import RegularTeacher, SpecialtyTeacher, Professional, SchoolAdmin


def get_staff_subclass_from_user_id(user_id):
    
    owner = get_object_or_404(User, id=user_id)
    
    try:
        staff = owner.regularteacher
    except RegularTeacher.DoesNotExist:
        pass
    try:
        staff = owner.specialtyteacher
    except SpecialtyTeacher.DoesNotExist:
        pass
    try:
        staff = owner.professional
    except Professional.DoesNotExist:
        pass
    try:
        staff = owner.schooladmin
    except SchoolAdmin.DoesNotExist:
        pass

    return staff


def get_first_name(self):
    return self.first_name + " " + self.last_name


User.add_to_class("__str__", get_first_name)


class CodeEtudiant(models.Model):
    code = models.CharField(max_length=10)
    definition = models.CharField(max_length=250, null=True)
    
    def __str__(self):
        return self.code + " " + self.definition
    
    class Meta:
        ordering = ['definition']


class Student(models.Model):
    # TODO: change primary key to fiche
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    comite_clinique = models.BooleanField(default=False)
    date_ref_comite_clinique = models.DateField(null=True)
    plan_intervention = models.BooleanField(default=False)
    groupe_repere = models.ForeignKey('school.Group', on_delete=models.SET_NULL, blank=True, null=True, default=None)
    code = models.ForeignKey(CodeEtudiant, on_delete=models.SET_NULL, null=True, blank=True)
    fiche = models.CharField(max_length=20, null=True, unique=True)
    etat_situation = models.TextField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    lang = models.CharField(max_length=100, blank=True, null=True, default=None)
    is_student = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_is_student_changed = models.DateTimeField(null=True, blank=True, default=None)

    def get_queryset(self, request):
        # Filter the queryset to include only instances with is_active=True
        return super().get_queryset(request).filter(is_student=True)

    @property
    def age_past_september(self):
        return self._calculate_age_past_september()
    
    def get_full_name(self):
        return self.prenom + " " + self.nom

    def get_fields(self):
        fields_data = []

        for field in Student._meta.fields:
            field_name = field.name
            field_value = getattr(self, field_name)

            # Check if the field is a date or datetime field
            if isinstance(field_value, (date, datetime)):
                field_value_str = field_value.isoformat()
            else:
                field_value_str = str(field_value)

            fields_data.append((field_name, field_value_str))

        return fields_data
    
    def _calculate_age_past_september(self):
        today = date.today()
        september_last_year = date(today.year - 1, 9, 1)
        if today < september_last_year:
            age = today.year - self.dob.year - 2
        else:
            age = today.year - self.dob.year - 1
        return age
    
    def get_absolute_url(self):
        return reverse('student-detail', kwargs={'pk': self.pk})

    def get_inactive_problems_query_set(self):
        return self.problematique_set.filter(status__nom="réglé")

    def get_active_problems_query_set(self):
        return self.problematique_set.filter(~Q(status__nom="réglé"))
    
    @property
    def get_etat_de_la_situation_entries(self):
        self.etatdelasituation_set.all()
    @property
    def get_professionals_from_actions(self):
        """Trouve les professionels impliqué dans les actions
        associées aux problematiques de l'éleve 
        """
        intervenants_set = set()
        class_set = set()
        for problematique in self.problematique_set.all():
            # print(problematique, problematique.action_set.all())
            for action in problematique.action_set.exclude(status__id=4):
                owner = get_staff_subclass_from_user_id(action.responsable.id)
                if isinstance(owner, Professional):  
                    intervenants_set.add(owner)
                    # print(action.responsable.get_full_name())
        return intervenants_set
    
    @property
    def responsible_personnel(self):
        try:
            directions = self.groupe_repere.classification.owner.get_full_name()
            regular_teachers = self.groupe_repere.regularteacher
            professional_list = self.get_professionals_from_actions
        except:
            directions = []
            regular_teachers = []
            professional_list = []
       

        return {
            'direction': directions,
            'regular_teachers': regular_teachers,
            # 'specialty_teachers': specialty_teachers,
            'professional_list': professional_list,
        }
    
    class Meta:
        ordering = ['nom', 'prenom']

    def __str__(self):
        return self.nom + " - " + self.prenom + " gr." + self.groupe_repere.nom if self.groupe_repere else "No group" + " ( Comité Clinique: " + str(self.comite_clinique) + " - PI: " + str(self.plan_intervention) + ")"


class EtatDeLaSituation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    text = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_entries')
    creation_date = models.DateField(auto_now_add=True)  # Changed to DateField
    modifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_entries')
    modification_date = models.DateField(auto_now=True)  # Changed to DateField

    def __str__(self):
        return f'Journal Entry by {self.creator}'

    class Meta:
        ordering = ['-modification_date']
        # unique_together = ('student', 'creator', 'creation_date') 


class StatusProblematique(models.Model):
    nom = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nom

    
class Problematique(models.Model):
    nom = models.ForeignKey(Item, on_delete=models.CASCADE)
    status = models.ForeignKey(StatusProblematique, on_delete=models.CASCADE)
    instigateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    detail = models.TextField(null=True, blank=True)
    eleve = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
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
    problematique = models.ForeignKey(Problematique, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = [['description', 'problematique']]
        ordering = ['problematique']

    def __str__(self):
        return self.problematique.eleve.nom + " " + self.problematique.eleve.prenom + " " + self.description[:50] + " *- Status -* " + self.status.nom


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
