from django.urls import path
from .views import LocalListView, LocalDetailView, LocalCreateView, LocalUpdateView, LocalDeleteView

urlpatterns = [
    path('local/list', LocalListView.as_view(), name='local_list'),
    path('local/<int:pk>/', LocalDetailView.as_view(), name='local_detail'),
    path('local/new/', LocalCreateView.as_view(), name='local_create'),
    path('local/<int:pk>/edit/', LocalUpdateView.as_view(), name='local_edit'),
    path('local/<int:pk>/delete/', LocalDeleteView.as_view(), name='local_delete'),
]
