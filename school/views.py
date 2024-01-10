from django.shortcuts import render
# from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from .models import Local, Matiere

from .my_functions import upload_data_from_excel


class LocalListView(ListView):
    model = Local
    template_name = 'local_list.html'

class LocalDetailView(DetailView):
    model = Local
    template_name = 'local_detail.html'

class LocalCreateView(CreateView):
    model = Local
    template_name = 'local_form.html'
    fields = ['nom', 'capacity']
    success_url = reverse_lazy('local_list')

class LocalUpdateView(UpdateView):
    model = Local
    template_name = 'local_form.html'
    fields = ['nom', 'capacity']
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
            upload_data_from_excel(excel_file)
            return HttpResponseRedirect(reverse('matiere_list'))  # Redirect to success page
    else:
        form = UploadFileForm()
    return render(request, 'school/matiere/upload_matiere_excel.html', {'form': form})

class MatiereListView(ListView):
    model = Matiere
    template_name = 'school/matiere/list_view.html'
