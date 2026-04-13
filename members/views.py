from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, EditProfileForm


def home(request):
    return render(request, 'members/home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
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
            return redirect('home')
        else:
            error_message = 'Invalid username or password.'

    return render(request, 'members/login.html', {'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('home')


def reset_password(request):
    return render(request, 'members/reset_password.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            form.save(request.user)
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user, user=request.user)

    return render(request, 'members/edit_profile.html', {'form': form})