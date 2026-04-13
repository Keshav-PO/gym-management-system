from django.shortcuts import render


def home(request):
    return render(request, 'members/home.html')


def register(request):
    return render(request, 'members/register.html')


def login_view(request):
    return render(request, 'members/login.html')