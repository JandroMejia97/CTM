from django.shortcuts import render

def home(request):
    return render(request, 'general/home.html', {'nav_active': 'home'})

def about(request):
    return render(request, 'general/about.html', {'nav_active': 'about'})

