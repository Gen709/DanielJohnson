from django.contrib import admin

# Register your models here.
from .models import Classification, Group, Local, Matiere, Competence, CategorieEmplois, CompetencesEvaluees
 
model_list = [Classification, Group, Local, Matiere, Competence, CategorieEmplois, CompetencesEvaluees]

# Register your models here.

for model in model_list:
    admin.site.register(model)