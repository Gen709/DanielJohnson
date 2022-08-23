from django.urls import path

from . import views

urlpatterns = [
    path('ajax/', views.ajax_search_problematiques, name='ajax-search-problematiques'),
]