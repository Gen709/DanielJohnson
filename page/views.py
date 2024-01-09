from django.shortcuts import render, redirect
from student.models import Action, StatusAction, Student
from django.views.decorators.csrf import csrf_exempt

from django.http.response import JsonResponse, HttpResponse

from django.db.models import Q, Count


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('home', pk=request.user.id)
    else:
        # return HttpResponse("Hello, world. You're NOT AUTHENTICATED.")
        return redirect('login')


def user_detail(request, pk):
    statusaction = StatusAction.objects.all()
    action_resp = Action.objects.filter(~Q(status__nom="terminé"), Q(responsable__id=1), Q(problematique__eleve__is_student=True)).order_by("problematique__eleve__nom")
    # Your queryset to group by 'responsable'
    grouped_actions = Action.objects.values('responsable').annotate(action_count=Count('id'))
    action_createur = Action.objects.filter(~Q(status__nom="terminé"), ~Q(responsable__id = pk), Q(createur__id = pk), Q(problematique__eleve__is_student=True)).order_by("responsable__last_name")
    responsables = action_createur.values_list('responsable__first_name', "responsable__last_name").distinct()
    context = {'id': pk,
               'action_resp': action_resp,
               'action_createur': action_createur,
               'statusaction': statusaction,
               'responsables': responsables
               }

    return render(request, 'page/user_detail.html', context)


@csrf_exempt
def ajax_etat_situation_save_view(request):
    if request.method == "POST":
        etat_situation_str = request.POST.get('etatdelasituation')
        student_id = request.POST.get('student_id')
        s = Student.objects.get(id=student_id)
        s.etat_situation = etat_situation_str
        s.save()

        data_list = [{'etat_situation_str': etat_situation_str},
                     {'student_id': student_id}
                     ]
        data = JsonResponse(data_list, safe=False)
        mimetype = 'application/json'

        return HttpResponse(data, mimetype)
