from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    
    
    def get_success_url(self):
        return reverse_lazy('index') 
    
    template_name = 'registration/login.html'

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

class ProfessionalProfileView(TemplateView):
    template_name = 'professional_profile.html'