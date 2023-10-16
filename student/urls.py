from django.urls import path

from . import views

urlpatterns = [
    path('ajax/', views.ajax_search_student, name='ajax-search-student'),
    path('ajax/update', views.ajax_update_student, name='ajax-update-student'),

    path('ajax/notes/', views.ajax_note_student, name='ajax-note-student'),

    path('problematique/ajax/update', views.ajax_student_problematique_update, name='ajax-student-problematique-update'),
    path('problematique/status/ajax/update', views.student_problematique_update_status, name='ajax-student-problematique-status-update'),
    path('problematique/action/status/ajax/update', views.ajax_student_problematique_action_status_update, name='ajax-student-problematique-action-status-update'),
    path('problematique/action/detail/ajax/update', views.ajax_student_problematique_action_detail_update, name='ajax-student-problematique-action-detail-update'),


    
    path('ajax/action/suggestions', views.ajax_search_probleme_action_sugestions, name='ajax-search-probleme-suggestions'),
    path('detail/<int:pk>', views.student_detail_view_2, name='student-detail'),
    path('problematique/create', views.student_problematique_create_view, name='problematique-create'),
    path('problematique/action/create', views.student_action_problematique_insert_view, name='action-create'),
    # path('comite_clinique/list', views.ComiteCliniqueStudentListView.as_view(), name='comite-clinique-list'),
    path('comite_clinique/list', views.comitecliniquestudentlistview, name='comite-clinique-list'),
    path('comite_clinique/data/excel_download', views.download_excel_data, name='comite-clinique-excel-download-data'),


    path('evaluation/list', views.eleve_evaluation_list, name='evaluation-list'),
    path('problematiques/list', views.eleve_problematique_list_view, name='problematique-list'),
    
    path('cours_ete/list', views.cours_ete_list_view, name='coursdete-list'),
    
    path('csv_uplaod', views.upload_csv, name='student-csv-uplaod'),
    path('review_changes/', views.review_changes, name='review_changes'),
    path('summary/', views.upload_summary, name='upload_summary'),

    path('etat/<int:id>', views.test_eta_de_la_situation, name='test_etat'),
]