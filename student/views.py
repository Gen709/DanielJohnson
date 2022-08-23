from django.shortcuts import render
from .models import Student
from urllib.parse import unquote

# Create your views here.

from django.http.response import JsonResponse, HttpResponse


def home(request):
    return HttpResponse("Hello, world. You're at the polls index.")


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
    
    student = Student.objects.get(pk=pk)
    
    context = {'student': student}
    
    return render(request, 'student/detail.html', context)