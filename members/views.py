from django.shortcuts import render


def home(request):
    return render(request, 'members/home.html')


def register(request):
    return render(request, 'members/register.html')


def login_view(request):
    return render(request, 'members/login.html')


def reset_password(request):
    return render(request, 'members/reset_password.html')


def edit_profile(request):
    return render(request, 'members/edit_profile.html')