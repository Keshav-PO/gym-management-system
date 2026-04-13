from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, EditProfileForm

from classes_app.models import GymClass
from subscriptions.models import MembershipPlan
from billing.models import Payment
from trainers.models import Trainer


def home(request):
    return render(request, 'members/home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'members/register.html', {'form': form})


def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = 'Invalid username or password.'

    return render(request, 'members/login.html', {'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('home')


def reset_password(request):
    success_message = None
    error_message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            success_message = 'Password reset successful. You can now log in with your new password.'
        except User.DoesNotExist:
            error_message = 'No user account was found with that email address.'

    return render(
        request,
        'members/reset_password.html',
        {
            'success_message': success_message,
            'error_message': error_message
        }
    )


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            form.save(request.user)
            return redirect('dashboard')
    else:
        form = EditProfileForm(instance=request.user, user=request.user)

    return render(request, 'members/edit_profile.html', {'form': form})


@login_required
def dashboard(request):
    context = {
        'total_members': User.objects.count(),
        'total_plans': MembershipPlan.objects.count(),
        'total_payments': Payment.objects.count(),
        'total_trainers': Trainer.objects.count(),
        'total_classes': GymClass.objects.count(),
    }
    return render(request, 'dashboard.html', context)