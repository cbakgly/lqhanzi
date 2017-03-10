from django.shortcuts import render


def index(request):
    return render(request, 'm2_help.html')
