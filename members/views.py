from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import RegisterForm, EditProfileForm
from .models import MemberProfile

from classes_app.models import GymClass, ClassRegistration
from subscriptions.models import MembershipPlan, Subscription
from billing.models import Payment
from trainers.models import Trainer


def home(request):
    return render(request, 'members/home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('home')
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

            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('home')

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
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            form.save(request.user)
            return redirect('member_dashboard')
    else:
        form = EditProfileForm(instance=request.user, user=request.user)

    return render(request, 'members/edit_profile.html', {'form': form})


@login_required
def admin_dashboard(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('member_dashboard')

    context = {
        'total_members': User.objects.filter(is_staff=False, is_superuser=False).count(),
        'total_plans': MembershipPlan.objects.count(),
        'total_payments': Payment.objects.count(),
        'total_trainers': Trainer.objects.count(),
        'total_classes': GymClass.objects.count(),
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def member_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_dashboard')

    profile = MemberProfile.objects.filter(user=request.user).first()

    active_subscription = Subscription.objects.filter(
        member=request.user,
        status='Active'
    ).select_related('plan').first()

    my_classes_count = ClassRegistration.objects.filter(
        member=request.user
    ).count()

    context = {
        'fitness_goal': profile.fitness_goal if profile else 'Not set',
        'experience_level': profile.experience_level if profile else 'Not set',
        'my_subscription': active_subscription.plan.name if active_subscription else 'No active subscription',
        'my_classes_count': my_classes_count,
    }
    return render(request, 'member/dashboard.html', context)