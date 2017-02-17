from django.shortcuts import render


def help(request):
    return render(request, 'hanzi_help.html')
