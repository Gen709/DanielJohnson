from django.contrib import admin

# Register your models here.
from .models import Classification, Group, Local
 
model_list = [Classification, Group, Local]

# Register your models here.

for model in model_list:
    admin.site.register(model)