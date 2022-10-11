from django.urls import path

from . import views

urlpatterns = [
    path('ajax/', views.ajax_search_student, name='ajax-search-student'),
    path('ajax/update', views.ajax_update_student, name='ajax-update-student'),
    path('problematique/ajax/update', views.ajax_student_problematique_update, name='ajax-student-problematique-update'),
    path('problematique/status/ajax/update', views.student_problematique_update_status, name='ajax-student-problematique-status-update'),
    path('problematique/action/status/ajax/update', views.ajax_student_problematique_action_status_update, name='ajax-student-problematique-action-status-update'),
    
    path('ajax/action/suggestions', views.ajax_search_probleme_action_sugestions, name='ajax-search-probleme-suggestions'),
    path('detail/<int:pk>', views.student_detail_view, name='student-detail'),
    path('problematique/create', views.student_problematique_create_view, name='problematique-create'),
    path('problematique/action/create', views.student_action_problematique_insert_view, name='action-create'),
    # path('comite_clinique/list', views.ComiteCliniqueStudentListView.as_view(), name='comite-clinique-list'),
    path('comite_clinique/list', views.comitecliniquestudentlistview, name='comite-clinique-list'),
    path('comite_clinique/data/excel_download', views.download_excel_data, name='comite-clinique-excel-download-data'),


    path('evaluation/list', views.eleve_evaluation_list, name='evaluation-list'),
    path('problematiques/list', views.eleve_problematique_list_view, name='problematique-list'),
    
    path('cours_ete/list', views.cours_ete_list_view, name='coursdete-list'),
]