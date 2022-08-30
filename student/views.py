from django.shortcuts import render
from .models import Student, CodeEtudiant
from urllib.parse import unquote
from django.contrib.auth.models import User
from django.views.generic.list import ListView



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
    
    student = Student.objects.get(pk=pk)
    
    context = {'student': student,
               'staff': staff}
    
    return render(request, 'student/detail.html', context)

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
    
            
    