from django.urls import path

from . import views

urlpatterns = [
    path('ajax/', views.ajax_search_student, name='ajax-search-student'),
    path('ajax/action/suggestions', views.ajax_search_probleme_action_sugestions, name='ajax-search-probleme-suggestions'),
    path('detail/<int:pk>', views.student_detail_view, name='student-detail'),
    path('problematique/create', views.student_problematique_create_view, name='problematique-create'),
    path('problematique/action/create', views.student_action_problematique_insert_view, name='action-create'),
    # path('comite_clinique/list', views.ComiteCliniqueStudentListView.as_view(), name='comite-clinique-list'),
    path('comite_clinique/list', views.comitecliniquestudentlistview, name='comite-clinique-list'),
    path('evaluation/list', views.eleve_evaluation_list, name='evaluation-list'),
]