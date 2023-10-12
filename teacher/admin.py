from django.contrib import admin

# Register your models here.
from .models import RegularTeacher, Professional, SchoolAdmin, SpecialtyTeacher

model_list = [RegularTeacher, Professional, SchoolAdmin, SpecialtyTeacher]

for model in model_list:
    admin.site.register(model)