from django.urls import path
from . import views

urlpatterns = [
    path('', views.trainer_dashboard, name='trainer_dashboard'),
    path('assignments/', views.trainer_assignments, name='trainer_assignments'),
    path('hours/', views.trainer_hours, name='trainer_hours'),
]