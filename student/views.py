from django.shortcuts import render, redirect
from django.db.models import Count
from urllib.parse import unquote
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Student, StatusAction, Problematique, StatusProblematique, Action, ActionSuggestion, CodeEtudiant
from problematiques.models import Item
from school.models import Classification
# Create your views here.
@csrf_exempt
def ajax_student_problematique_update(request):
    if request.method == "POST":
        problematique_id = request.POST.get("problematique_id", "No problematique id")
        p = Problematique.objects.get(id=problematique_id)
        problematique_desc = request.POST.get("problematique_desc", "No problematique desc")
        p.detail = problematique_desc
        p.save()
    return render(request, "student/prob_erreur.html")


def ajax_search_probleme_action_sugestions(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # input_str = request.GET.get('term', '')
        input_str = unquote(request.GET['term'])
        data_list = [{x.id: {'description': x.nom}} for x in
                     ActionSuggestion.objects.filter(nom__istartswith=input_str)]

        data = JsonResponse(data_list, safe=False)

        mimetype = 'application/json'

        if len(data_list) > 0 and input_str != '':
            return HttpResponse(data, mimetype)
        else:
            data = JsonResponse([{'description': 'Aucune suggestion'}], safe=False)
            return HttpResponse(data, mimetype)


def ajax_search_student(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # input_str = request.GET.get('term', '')
        input_str = unquote(request.GET['term'])
        data_list = [{x.id: {'description': x.nom + " " + x.prenom + " - Group: " + x.groupe_repere,
                             'url': x.get_absolute_url()}} for x in Student.objects.filter(nom__istartswith=input_str)]

        data = JsonResponse(data_list, safe=False)

        mimetype = 'application/json'
        if len(data_list) > 0 and input_str != '':
            return HttpResponse(data, mimetype)
        else:
            data = JsonResponse([{'description': "Nothing with the term " + input_str,
                                  'url': "NO URL"}], safe=False)
            return HttpResponse(data, mimetype)


def ajax_update_student(request):
    parameter = unquote(request.GET.get('param'))
    value = unquote(request.GET.get('value'))
    student_id = unquote(request.GET.get('student_id'))

    s = Student.objects.get(pk=student_id)

    if parameter == "comite_cliniqueflexSwitchCheck":
        s.comite_clinique = value
    elif parameter == "plan_interventionRadioOptionsflexSwitchCheck":
        s.plan_intervention = value
    elif parameter == "student_code":
        c = CodeEtudiant.objects.get(pk=value)
        s.code = c

    s.save()

    return redirect('student-detail', pk=student_id)


@login_required
def student_detail_view(request, pk):
    # a revoir
    staff = User.objects.get(username=request.user.get_username())

    responsable_qs = User.objects.all()

    student = Student.objects.get(pk=pk)

    problematiques = Item.objects.all()

    statusproblematique = StatusProblematique.objects.all()

    statusaction = StatusAction.objects.all()

    code_etudiant = CodeEtudiant.objects.all()

    context = {'student': student,
               'staff': staff,
               'problematiques': problematiques,
               'statusaction': statusaction,
               'statusproblematique': statusproblematique,
               'responsable_qs': responsable_qs,
               'code_etudiant': code_etudiant
               }

    return render(request, 'student/detail.html', context)

@login_required
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

@login_required
def student_action_problematique_insert_view(request):
    student = Student.objects.get(pk=request.POST.get("eleve_id"))
    staff = User.objects.get(pk=request.POST.get("staff_id"))
    problematique = Problematique.objects.get(pk=request.POST.get("problematique_id"))
    description = request.POST.get("description")
    detail = request.POST.get("detail")
    action_status = StatusAction.objects.get(pk=request.POST.get("action_status_id"))
    responsable = User.objects.get(pk=request.POST.get("responsable_id"))

    a = Action(createur=staff,
               responsable=responsable,
               description=description,
               detail=detail,
               status=action_status,
               problematique=problematique)
    a.save()

    return redirect(student.get_absolute_url())


@login_required
def comitecliniquestudentlistview(request):
    student_comite_clinique_dict = {
        classification: [s for s in Student.objects.filter(classification=classification).filter(comite_clinique=True)]
        for classification in
        {c for c in Classification.objects.filter(student__comite_clinique=True)}
    }

    context = {'student_comite_clinique_dict': student_comite_clinique_dict}

    return render(request, "student/comite_clinique_list.html", context)


@login_required
def cours_ete_list_view(request):
    context = {}
    return render(request, 'student/coursdete_eleve.html', context)


@login_required
def eleve_evaluation_list(request):
    suggestion_list = ActionSuggestion.objects.all()
    a = Action.objects.filter(description__in=[x.nom for x in suggestion_list])

    context = {'evaluation_suggestion_list': suggestion_list,
               'evaluation_liste': a
               }

    return render(request, 'student/evaluation_eleve.html', context)


@login_required
def eleve_problematique_list_view(request):
    code_etudiant_qs = CodeEtudiant.objects.exclude(code=0).annotate(num_student=Count('student'))

    results = {code: {classification:
                          [student for student in code.student_set.all().filter(classification=classification.id)]
                      for classification in {etudiant.classification for etudiant in code.student_set.all()}
                      }
               for code in code_etudiant_qs
               }
    # classification_list = problematique_list.student.classification.distinct()

    # classification = CodeEtudiant.objects.
    context = {"results": results
               # "classification_list":test
               }

    return render(request, 'student/problemes_eleve.html', context)
