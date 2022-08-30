from django.contrib import admin

from .models import Student, StatusAction, StatusProblematique, Action, Problematique, CodeEtudiant, ActionSuggestion

model_list = [Student, StatusAction, StatusProblematique, Action, Problematique, CodeEtudiant, ActionSuggestion]

# Register your models here.

for model in model_list:
    admin.site.register(model)