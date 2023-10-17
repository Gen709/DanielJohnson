from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from school.models import Group, Classification

from .forms import CSVUploadForm
from .util import ExtractTeacher


class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user

        # if hasattr(user, 'schooladmin'):
        #     return redirect('schooladmin_dashboard_url')

        if hasattr(user, 'regularteacher'):
            return redirect('regular_teacher_profile')
        
        if hasattr(user, 'specialtyteacher'):
            return redirect('specialty_teacher_profile')
        
        if hasattr(user, 'professional'):
            return redirect('professional_profile')

        # If user doesn't match any specific type, go to a default dashboard
        return redirect('index')


class RegularTeacherProfileView(TemplateView):
    template_name = 'regular_teacher_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assuming you pass the teacher instance to this view through the context
        context['teacher'] = self.request.user.regularteacher  # Assuming the teacher is associated with the logged-in user
        return context


class SpecialtyTeacherProfileView(TemplateView):
    template_name = 'specialty_teacher_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assuming you pass the teacher instance to this view through the context
        context['teacher'] = self.request.user.specialityteacher  # Assuming the teacher is associated with the logged-in user
        return context


class ProfessionalProfileView(TemplateView):
    template_name = 'professional_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assuming you pass the teacher instance to this view through the context
        context['teacher'] = self.request.user.professional  # Assuming the teacher is associated with the logged-in user
        return context


@login_required
def upload_teacher_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            es = ExtractTeacher(request)
            context = es.update_data()
            # if len(context["updated_regular_teacher"]) == 0:
            #     message = "No teacher has been added"
            # context["message"] = message
            return render(request, 'teacher/summary_page.html', context)
    else:
        
        orphan_groups = Group.objects.filter(classification=None)
        form = CSVUploadForm()
        context = {'form': form,
                   'orphan_groups_qs': orphan_groups,
                   'orphan_classifications_qs': Classification.objects.filter(owner=None)
                   }
    return render(request, 'teacher/upload_csv.html', context)