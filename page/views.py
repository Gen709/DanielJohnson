from django.shortcuts import render, redirect
from student.models import Action, StatusAction, Student
from django.views.decorators.csrf import csrf_exempt

from django.http.response import JsonResponse, HttpResponse

# Create your views here.



def index(request):
    if request.user.is_authenticated:
        return redirect('home', pk=request.user.id)
    else:
        # return HttpResponse("Hello, world. You're NOT AUTHENTICATED.")
        return redirect('login')

def user_detail(request, pk):
    statusaction = StatusAction.objects.all()
    action_resp = Action.objects.filter(responsable__id=pk)
    action_createur = Action.objects.filter(createur__id=pk)
    context = {'id': pk, 
               'action_resp': action_resp,
               'action_createur': action_createur
               
               }
    
    return render(request, 'page/user_detail.html', context)

def user_task(request, pk):
    pass
    
@csrf_exempt
def ajax_etat_situation_save_view(request):
    
    # if request.headers.post('x-requested-with') == 'XMLHttpRequest':
    #     # input_str = request.GET.get('term', '')
    #     data_list =[]
    #     etat_situation_str = request.POST['etatdelasituation']
    #     # data_list = [{x.id: {'description':x.nom + " " + x.prenom + " - Group: " + x.groupe_repere, 
    #     #                      'url': x.get_absolute_url()}} for x in Student.objects.filter(nom__istartswith=input_str)]
    #
    #     data_list = [{'etat_situation_str': etat_situation_str}]
    #     data = JsonResponse(data_list, safe=False)
    #
    #     mimetype = 'application/json'
    #     if len(data_list) > 0 and input_str != '':
    #         return HttpResponse(data, mimetype)
    #     else:
    #         return HttpResponse('', mimetype)
        
    # data_list =[]
    if request.POST.get('etatdelasituation'):
        etat_situation_str = request.POST.get('etatdelasituation')
        student_id = request.POST.get('student_id')
        crf_token = request.POST.get('csrfmiddlewaretoken')
        s = Student.objects.get(id=student_id)
        s.etat_situation = etat_situation_str
        s.save()
    else:
        etat_situation_str = "Le POST est NULL"
    # data_list = [{x.id: {'description':x.nom + " " + x.prenom + " - Group: " + x.groupe_repere, 
    #                      'url': x.get_absolute_url()}} for x in Student.objects.filter(nom__istartswith=input_str)]
    data_list = [{'etat_situation_str': etat_situation_str}, 
                 {'student_id':student_id},
                 {'crf_token':crf_token}
                ]
    data = JsonResponse(data_list, safe=False)
    
    mimetype = 'application/json'
    if len(data_list) > 0 and etat_situation_str != '':
        return HttpResponse(data, mimetype)
    else:
        return HttpResponse('', mimetype)