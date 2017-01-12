# -*- coding:utf8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    return render(request, 'task_package_management.html')


@login_required
def business(request):
    return render(request, 'business.html')


@login_required
def task(request):
    return render(request, 'task.html')


@login_required
def clock(request):
    return render(request, 'clock.html')


@login_required
def integral(request):
    return render(request, 'integral.html')


@login_required
def award(request):
    return render(request, 'award.html')


@login_required
def usertake(request):
    return render(request, 'usertake.html')


@login_required
def privelegs(request):
    return render(request, 'privelegs.html')


@login_required
def parts(request):
    return render(request, 'parts.html')


@login_required
def radical(request):
    return render(request, 'radical.html')


@login_required
def type_data_dictionary(request):
    return render(request, 'type_data_dictionary.html')


@login_required
def take(request):
    return render(request, 'take.html')
