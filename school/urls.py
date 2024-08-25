from django.urls import path
from .views import LocalListView, LocalDetailView, LocalCreateView, LocalUpdateView, LocalDeleteView, upload_matiere_file,\
MatiereListView, update_cours_is_active

urlpatterns = [
    path('local/list', LocalListView.as_view(), name='local_list'),
    path('local/<int:pk>/', LocalDetailView.as_view(), name='local_detail'),
    path('local/new/', LocalCreateView.as_view(), name='local_create'),
    path('local/<int:pk>/edit/', LocalUpdateView.as_view(), name='local_edit'),
    path('local/<int:pk>/delete/', LocalDeleteView.as_view(), name='local_delete'),
    path('matiere/uplaod', upload_matiere_file, name='upload_matiere_excel'),
    path('matiere/list', MatiereListView.as_view(), name='matiere_list'),
    path('matiere/is_active/', update_cours_is_active, name='update_cours_is_active'),
]


