from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import GymClass, ClassRegistration
from .forms import GymClassForm


def class_list(request):
    classes = GymClass.objects.all().order_by('class_date', 'class_time')
    return render(request, 'classes_app/class_list.html', {'classes': classes})


@login_required
def class_create(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('member_dashboard')

    if request.method == 'POST':
        form = GymClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = GymClassForm()

    return render(request, 'classes_app/class_form.html', {'form': form, 'page_title': 'Add Class'})


@login_required
def register_class(request, class_id):
    gym_class = get_object_or_404(GymClass, id=class_id)

    already_registered = ClassRegistration.objects.filter(
        member=request.user,
        gym_class=gym_class
    ).exists()

    current_count = ClassRegistration.objects.filter(gym_class=gym_class).count()

    if not already_registered and current_count < gym_class.capacity:
        ClassRegistration.objects.create(member=request.user, gym_class=gym_class)

    return redirect('my_classes')


@login_required
def my_classes(request):
    registrations = ClassRegistration.objects.filter(member=request.user).order_by('-registered_at')
    return render(request, 'classes_app/my_classes.html', {'registrations': registrations})