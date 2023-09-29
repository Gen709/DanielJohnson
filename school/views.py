from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Local

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
