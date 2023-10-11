# yourapp/teacher_urls.py (inside your app directory)

from django.urls import path
from .views import (
    RegularTeacherProfileView,
    SpecialtyTeacherProfileView,
    ProfessionalProfileView,
    upload_teacher_csv
)


urlpatterns = [
    path('regular_teacher_profile/', RegularTeacherProfileView.as_view(), name='regular_teacher_profile'),
    path('specialty_teacher_profile/', SpecialtyTeacherProfileView.as_view(), name='specialty_teacher_profile'),
    path('professional_profile/', ProfessionalProfileView.as_view(), name='professional_profile'),
    path('uplaod_teacher_extract/', upload_teacher_csv, name='teacher_csv_uplaod'),
]