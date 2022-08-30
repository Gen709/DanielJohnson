from django.shortcuts import render, redirect
from .models import Student, StatusAction, Problematique, StatusProblematique, Action
from problematiques.models import Item
from urllib.parse import unquote
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.contrib.auth.models import User



# Create your views here.

from django.http.response import JsonResponse, HttpResponse


def ajax_search_student(request):
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # input_str = request.GET.get('term', '')
        data_list =[]
        input_str = unquote(request.GET['term'])
        data_list = [{x.id: {'description':x.nom + " " + x.prenom + " - Group: " + x.groupe_repere, 
                             'url': x.get_absolute_url()}} for x in Student.objects.filter(nom__istartswith=input_str)]
    
        data = JsonResponse(data_list, safe=False)
        
        mimetype = 'application/json'
        if len(data_list) > 0 and input_str != '':
            return HttpResponse(data, mimetype)
        else:
            return HttpResponse('', mimetype)
    

def student_detail_view(request, pk):
    
    staff = User.objects.get(username = request.user.get_username())
    
    responsable_qs = User.objects.all()
    
    student = Student.objects.get(pk=pk)
    
    problematiques = Item.objects.all()
    
    statusproblematique = StatusProblematique.objects.all()
    
    statusaction = StatusAction.objects.all()
    
    context = {'student': student,
               'staff': staff,
               'problematiques': problematiques,
               'statusaction': statusaction, 
               'statusproblematique':statusproblematique,
               'responsable_qs':responsable_qs
               }
    
    return render(request, 'student/detail.html', context)

def student_problematique_create_view(request):
    student = Student.objects.get(pk=request.POST.get("eleve_id"))
    instigateur = User.objects.get(pk=request.POST.get("staff_id"))
    problematique = Item.objects.get(pk=request.POST.get("problematique_id"))
    detail = request.POST.get("prob_detail")
    status = StatusProblematique.objects.get(pk=request.POST.get("status_prob"))
    
    p = Problematique(nom=problematique, 
                      status=status, 
                      instigateur=instigateur,
                      detail=detail, 
                      eleve=student)
    p.save()
    
    return redirect(student.get_absolute_url())

def student_action_problematique_insert_view(request):
    student = Student.objects.get(pk=request.POST.get("eleve_id"))
    staff = User.objects.get(pk=request.POST.get("staff_id"))
    problematique = Problematique.objects.get(pk=request.POST.get("problematique_id"))
    description = request.POST.get("description")
    detail = request.POST.get("detail")
    action_status = StatusAction.objects.get(pk=request.POST.get("action_status_id"))
    responsable =  User.objects.get(pk=request.POST.get("responsable_id"))
    
    a = Action(createur=staff, 
               responsable=responsable, 
               description=description, 
               detail=detail, 
               status=action_status, 
               problematique=problematique)
    a.save()
    # 
    # 
    # 
    # 
    # 
    # 
    
    return redirect(student.get_absolute_url())

# class ComiteCliniqueStudentListView(ListView):
#     model=Student
#     context_object_name = 'student_list'
#     template_name = "student/comite_clinique_liste.html"
#
#     def get_queryset(self):
#         return Student.objects.filter(comite_clinique=True)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['niveau'] = CodeEtudiant.objects.all()
#         return context
        
def comitecliniquestudentlistview(request):
    student = Student.objects.filter(comite_clinique=True)
    classification_list = set([x for x in Student.objects.all().values_list('classification', flat=True)])
    context = {'student': student,
               'niveau': classification_list}
    
    return render(request, "student/comite_clinique_accordeon.html", context)
    
            
    