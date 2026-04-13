from django.shortcuts import render
from .models import TrainerAssignment, TrainerHour


def trainer_assignments(request):
    assignments = TrainerAssignment.objects.select_related('trainer', 'gym_class').all().order_by('-assigned_date')
    return render(request, 'trainers/trainer_assignments.html', {'assignments': assignments})


def trainer_hours(request):
    hours = TrainerHour.objects.select_related('trainer', 'gym_class').all().order_by('-work_date')
    return render(request, 'trainers/trainer_hours.html', {'hours': hours})

def trainer_dashboard(request):
    return render(request, 'trainers/dashboard.html')