from django.shortcuts import render, redirect
from django.db.models import Count
from urllib.parse import unquote
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Student, StatusAction, Problematique, StatusProblematique, Action, ActionSuggestion, CodeEtudiant, Grades
from problematiques.models import Item
from school.models import Classification

from datetime import datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Alignment
import re


# Create your views here.
@csrf_exempt
def ajax_student_problematique_action_detail_update(request):
    if request.method == "POST":
        a = Action.objects.get(id=int(request.POST.get('action_id', "").split("_")[2]))
        detail = request.POST.get('action_desc', "")

        a.detail = detail
        a.save()

        return redirect(a.problematique.eleve.get_absolute_url())


@csrf_exempt
def ajax_student_problematique_action_status_update(request):
    if request.method == "POST":
        a = Action.objects.get(id=int(request.POST.get('action_id', "").split("_")[2]))
        s = StatusAction.objects.get(id=request.POST.get('status_id', ""))

        a.status = s
        a.save()

        return redirect(a.problematique.eleve.get_absolute_url())


@csrf_exempt
def ajax_student_problematique_update(request):
    if request.method == "POST":
        problematique_id = request.POST.get("problematique_id", "No problematique id")
        p = Problematique.objects.get(id=problematique_id)
        problematique_desc = request.POST.get("problematique_desc", "No problematique desc")
        p.detail = problematique_desc
        p.save()
        return redirect(p.eleve.get_absolute_url())


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

@csrf_exempt
def ajax_note_student(request):
    student_id = request.POST.get("student_id")
    data_dict = {}
    # etudiant
    s = Student.objects.get(id=student_id)

    # niveau de l'??tudiant

    niveau = s.classification

    data_dict["niveau"] = niveau.nom

    # notes de l'ann??e en cour

    n = Grades.objects.filter(student_id=student_id)

    # liste des notes de l'??l??ve

    grades_list = [x.note for x in n]

    data_dict["grade_list"] = grades_list

    # liste des cours de l'??l??ve

    class_name_list = [x.matiere for x in n]

    classification_className_tuple_list = [(x.classification, x.matiere) for x in n]

    data_dict["class_name_list"] = class_name_list

    data_dict["classification_className_tuple_list"] = classification_className_tuple_list

    # Notes de groupe

    data_dict["class_grades"] = {}

    for classification_className_tuple in data_dict["classification_className_tuple_list"]:
        data_dict["class_grades"][classification_className_tuple[1]] = [x.note for x in Grades.objects.filter(
            matiere=classification_className_tuple[1])]

    data = JsonResponse(data_dict, safe=False)
    mimetype = 'application/json'
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


@csrf_exempt
def student_problematique_update_status(request):
    p = Problematique.objects.get(id=int(request.POST.get('problematique_id', "").split("_")[2])) # probleme
    s = StatusProblematique.objects.get(id=request.POST.get('status_id', ""))
    p.status = s
    p.save()

    return redirect(p.eleve.get_absolute_url())


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


@login_required
def download_excel_data(request, user_id=None):
    def cleanhtml(raw_html):
        CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

        if raw_html != "" and (type(raw_html) == str):
            cleantext = re.sub(CLEANR, '', raw_html)
            return cleantext

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Comit??_Clinique_Daniel_Johnson_' + dt.now().strftime(
        "%Y-%m-%d %H:%M:%S") + ".xlsx"

    wb = Workbook()

    ws1 = wb.active
    ws1.title = "Comit?? Clinique"
    ws1['A1'] = "??tudiant"
    ws1.merge_cells(start_row=1, start_column=1, end_row=1, end_column=9)
    ws1['J1'] = "Probl??matiques"
    ws1.merge_cells(start_row=1, start_column=10, end_row=1, end_column=13)
    ws1['N1'] = "Action"
    ws1.merge_cells(start_row=1, start_column=14, end_row=1, end_column=18)

    c = ws1['A3']
    ws1.freeze_panes = c
    ws1['A2'] = "fiche"
    ws1['B2'] = "nom"
    ws1['C2'] = "prenom"
    ws1['D2'] = "groupe_repere"
    ws1['E2'] = "classification"
    ws1['F2'] = "comite_clinique"
    ws1['g2'] = "plan_intervention"
    ws1['h2'] = "etat_situation"
    ws1['i2'] = "classification"
    ws1['j2'] = "problematique_nom"
    ws1['k2'] = "problematique_status"
    ws1['l2'] = "problematique_instigateur"
    ws1['m2'] = "problematique_detail"
    ws1['n2'] = "action_createur"
    ws1['o2'] = "action_responsable"
    ws1['p2'] = "action_description"
    ws1['q2'] = "action_detail"
    ws1['r2'] = "action_status"

    i = 3

    for student in Student.objects.filter(comite_clinique=True).order_by('classification', 'nom'):
        if student.problematique_set.all():
            for problematique in student.problematique_set.all():
                if problematique.action_set.all():
                    for action in problematique.action_set.all():
                        ws1['A' + str(i)] = student.fiche
                        ws1['B' + str(i)] = student.nom
                        ws1['C' + str(i)] = student.prenom
                        ws1['D' + str(i)] = student.groupe_repere
                        ws1['E' + str(i)] = student.classification.nom
                        ws1['F' + str(i)] = student.comite_clinique
                        ws1['g' + str(i)] = student.plan_intervention
                        ws1['h' + str(i)] = cleanhtml(student.etat_situation)
                        ws1['h' + str(i)].alignment = Alignment(wrapText=True)
                        ws1['i' + str(i)] = student.classification.nom

                        ws1['j' + str(i)] = problematique.nom.nom
                        ws1['k' + str(i)] = problematique.status.nom
                        ws1['l' + str(i)] = problematique.instigateur.first_name
                        ws1['m' + str(i)] = cleanhtml(problematique.detail)
                        ws1['m' + str(i)].alignment = Alignment(wrapText=True)

                        ws1['n' + str(i)] = action.createur.first_name
                        ws1['o' + str(i)] = action.responsable.first_name
                        ws1['p' + str(i)] = action.description
                        ws1['q' + str(i)] = cleanhtml(action.detail)
                        ws1['q' + str(i)].alignment = Alignment(wrapText=True)
                        ws1['r' + str(i)] = action.status.nom
                        i += 1
                else:
                    ws1['A' + str(i)] = student.fiche
                    ws1['B' + str(i)] = student.nom
                    ws1['C' + str(i)] = student.prenom
                    ws1['D' + str(i)] = student.groupe_repere
                    ws1['E' + str(i)] = student.classification.nom
                    ws1['F' + str(i)] = student.comite_clinique
                    ws1['g' + str(i)] = student.plan_intervention
                    ws1['h' + str(i)] = cleanhtml(student.etat_situation)
                    ws1['h' + str(i)].alignment = Alignment(wrapText=True)
                    ws1['i' + str(i)] = student.classification.nom

                    ws1['j' + str(i)] = problematique.nom.nom
                    ws1['k' + str(i)] = problematique.status.nom
                    ws1['l' + str(i)] = problematique.instigateur.first_name
                    ws1['m' + str(i)] = cleanhtml(problematique.detail)
                    ws1['m' + str(i)].alignment = Alignment(wrapText=True)
                    i += 1

        else:
            ws1['A' + str(i)] = student.fiche
            ws1['B' + str(i)] = student.nom
            ws1['C' + str(i)] = student.prenom
            ws1['D' + str(i)] = student.groupe_repere
            ws1['E' + str(i)] = student.classification.nom
            ws1['F' + str(i)] = student.comite_clinique
            ws1['g' + str(i)] = student.plan_intervention
            ws1['h' + str(i)] = cleanhtml(student.etat_situation)
            ws1['h' + str(i)].alignment = Alignment(wrapText=True)
            ws1['i' + str(i)] = student.classification.nom
            i += 1



    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Comit??_Clinique_Daniel_Johnson_' + dt.now().strftime(
        "%Y-%m-%d %H:%M:%S")+'.xlsx'
    wb.save(filename=response)
    return response
