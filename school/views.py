from django.shortcuts import render
# from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from .forms import UploadFileForm
from .models import Local, Cours
from django.db.models import Q
from django.db.models.functions import Substr
from django.db.models import F


from .my_functions import  upload_data_from_excel_matiere, upload_data_from_excel_competences,\
    get_headings, matiere_headings_list, objectif_matiere_headings_list, upload_data_from_excel_objectifs_resultats


class LocalListView(ListView):
    model = Local
    template_name = 'local_list.html'

class LocalDetailView(DetailView):
    model = Local
    template_name = 'local_detail.html'

class LocalCreateView(CreateView):
    model = Local
    template_name = 'local_form.html'
    fields = '__all__'
    success_url = reverse_lazy('local_list')

class LocalUpdateView(UpdateView):
    model = Local
    template_name = 'local_form.html'
    fields = '__all__'
    success_url = reverse_lazy('local_list')

class LocalDeleteView(DeleteView):
    model = Local
    template_name = 'local_confirm_delete.html'
    success_url = reverse_lazy('local_list')

# Create your views here.

def upload_matiere_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file'].read()
            headings = get_headings(excel_file)
            if headings == matiere_headings_list:
                upload_data_from_excel_matiere(excel_file)
                reverse_url_name = 'matiere_list'
            elif headings == objectif_matiere_headings_list:
                upload_data_from_excel_competences(excel_file)
                upload_data_from_excel_objectifs_resultats(excel_file)
                reverse_url_name = 'matiere_list'
            return HttpResponseRedirect(reverse(reverse_url_name))  # Redirect to success page
    else:
        form = UploadFileForm()
    return render(request, 'school/matiere/upload_matiere_excel.html', {'form': form})

from django.db.models import Q
from django.db.models.functions import Substr

class MatiereListView(ListView):
    model = Cours
    template_name = 'school/matiere/list_view.html'

    def get_queryset(self):
        return super().get_queryset().order_by('matiere', 'Cours')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        niveau = self.request.GET.get('niveau') if self.request.GET.get('niveau') else ""

        if niveau == "diff":
            # Annotate with the 4th character
            annotated_qs = self.get_queryset().annotate(fourth_char=Substr('Cours', 4, 1))

            # Union of all other options
            union_qs = annotated_qs.filter(
                Q(Cours__endswith="DIM") | Q(Cours__endswith="TSA") | Q(Cours__endswith="000") |
                Q(fourth_char__in=["1", "2", "3", "4", "5"])
            )
            # Difference
            context['active_courses'] = self.get_queryset().filter(is_active=True).exclude(pk__in=union_qs)
            context['inactive_courses'] = self.get_queryset().filter(is_active=False).exclude(pk__in=union_qs)

            context['template_actifs'] = 'school/matiere/cours_actifs_filtered.html'
            context['template_inactifs'] = 'school/matiere/cours_inactifs_filtered.html'
        elif niveau == "":
            # All courses
            context['active_courses'] = self.get_queryset().filter(is_active=True)
            context['inactive_courses'] = self.get_queryset().filter(is_active=False)

            context['template_actifs'] = 'school/matiere/cours_actifs.html'
            context['template_inactifs'] = 'school/matiere/cours_inactifs.html'
        else:
            # Filter by specific niveau
            if niveau in ["DIM", "TSA", "000"]:
                context['active_courses'] = self.get_queryset().filter(is_active=True, Cours__endswith=niveau)
                context['inactive_courses'] = self.get_queryset().filter(is_active=False, Cours__endswith=niveau)
            else:
                context['active_courses'] = self.get_queryset().annotate(
                    fourth_char=Substr('Cours', 4, 1)
                ).filter(is_active=True, fourth_char=niveau)
                context['inactive_courses'] = self.get_queryset().annotate(
                    fourth_char=Substr('Cours', 4, 1)
                ).filter(is_active=False, fourth_char=niveau)

            context['template_actifs'] = 'school/matiere/cours_actifs_filtered.html'
            context['template_inactifs'] = 'school/matiere/cours_inactifs_filtered.html'

        return context

        
    
def update_cours_is_active(request):
    if request.method == 'POST':
        cours_id = request.POST.get('cours_id')
        is_active = request.POST.get('is_active') == 'true'

        cours = Cours.objects.get(Cours=cours_id)
        cours.is_active = is_active
        cours.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request'})
