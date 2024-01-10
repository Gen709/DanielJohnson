from django import template

register = template.Library()

@register.filter(name='filter_responsable')
def filter_responsable(actions, responsible_name):
    return actions.filter(responsable__first_name=responsible_name)

@register.filter(name='filter_student')
def filter_student(actions, prenom):
    return actions.filter(problematique__eleve__prenom=prenom)

