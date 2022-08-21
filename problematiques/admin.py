from django.contrib import admin

from .models import Categorie, Item

# Register your models here.
admin.site.register(Categorie)
admin.site.register(Item)