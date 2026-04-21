from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Trainer, TrainerAssignment, TrainerHour
from classes_app.models import GymClass


@login_required
def trainer_dashboard(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('member_dashboard')

    total_assignments = TrainerAssignment.objects.count()
    total_hours = TrainerHour.objects.count()
    total_trainers = Trainer.objects.count()

    context = {
        'total_assignments': total_assignments,
        'total_hours': total_hours,
        'total_trainers': total_trainers,
    }
    return render(request, 'trainers/dashboard.html', context)


@login_required
def trainer_assignments(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('member_dashboard')

    assignments = TrainerAssignment.objects.select_related('trainer', 'gym_class').all().order_by('-assigned_date')
    return render(request, 'trainers/trainer_assignments.html', {'assignments': assignments})


@login_required
def assign_trainer(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('member_dashboard')

    trainers = Trainer.objects.all().order_by('name')
    classes = GymClass.objects.all().order_by('class_date', 'class_time')

    if request.method == 'POST':
        trainer_id = request.POST.get('trainer')
        class_id = request.POST.get('gym_class')

        already_assigned = TrainerAssignment.objects.filter(
            trainer_id=trainer_id,
            gym_class_id=class_id
        ).exists()

        if not already_assigned:
            TrainerAssignment.objects.create(
                trainer_id=trainer_id,
                gym_class_id=class_id
            )

        return redirect('trainer_assignments')

    return render(request, 'trainers/assign_trainer.html', {
        'trainers': trainers,
        'classes': classes
    })


@login_required
def trainer_hours(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('member_dashboard')

    hours = TrainerHour.objects.select_related('trainer', 'gym_class').all().order_by('-work_date')
    return render(request, 'trainers/trainer_hours.html', {'hours': hours})