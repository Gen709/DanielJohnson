from django.contrib import admin

# Register your models here.
from .models import Classification
 
model_list = [Classification]

# Register your models here.

for model in model_list:
    admin.site.register(model)