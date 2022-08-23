from django.urls import path

from . import views

urlpatterns = [
    path('ajax/', views.ajax_search_student, name='ajax-search-student'),
    path('detail/<int:pk>', views.student_detail_view, name='student-detail'),
]