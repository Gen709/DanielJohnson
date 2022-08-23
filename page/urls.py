from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'), # this redirect to user/profile
    path('user/profile/<int:pk>', views.user_detail, name='home'),
    path('user/task/<int:pk>', views.user_task, name='user-task'),
]