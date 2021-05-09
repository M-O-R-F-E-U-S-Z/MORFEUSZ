from django.shortcuts import render


def home(request):
    return render(request, 'morfeusz_app/home.html', {'title': 'Home Page'})
