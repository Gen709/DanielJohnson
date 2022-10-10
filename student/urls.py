from django.urls import path

from . import views

urlpatterns = [
    path('ajax/', views.ajax_search_student, name='ajax-search-student'),
    path('ajax/update', views.ajax_update_student, name='ajax-update-student'),
    path('problematique/ajax/update', views.ajax_student_problematique_update, name='ajax-student-problematique-update'),
    
    path('ajax/action/suggestions', views.ajax_search_probleme_action_sugestions, name='ajax-search-probleme-suggestions'),
    path('detail/<int:pk>', views.student_detail_view, name='student-detail'),
    path('problematique/create', views.student_problematique_create_view, name='problematique-create'),
    path('problematique/action/create', views.student_action_problematique_insert_view, name='action-create'),
    # path('comite_clinique/list', views.ComiteCliniqueStudentListView.as_view(), name='comite-clinique-list'),
    path('comite_clinique/list', views.comitecliniquestudentlistview, name='comite-clinique-list'),
    path('evaluation/list', views.eleve_evaluation_list, name='evaluation-list'),
    path('problematiques/list', views.eleve_problematique_list_view, name='problematique-list'),
    
    path('cours_ete/list', views.cours_ete_list_view, name='coursdete-list'),
]