# -*- coding:utf8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def task_package(request):
    return render(request, 'task_package.html')


@login_required
def task(request):
    return render(request, 'task.html')


@login_required
def check_in(request):
    return render(request, 'check_in_management.html')


@login_required
def credits(request):
    return render(request, 'credits.html')


@login_required
def reward(request):
    return render(request, 'reward.html')


@login_required
def user_management(request):
    return render(request, 'user_management.html')


@login_required
def access_privilege(request):
    return render(request, 'privileges.html')


@login_required
def hanzi_parts(request):
    return render(request, 'hanzi_parts.html')


@login_required
def hanzi_radicals(request):
    return render(request, 'hanzi_radicals.html')


@login_required
def task_type_management(request):
    return render(request, 'task_type_management.html')


@login_required
def forum(request):
    return render(request, 'forum_management.html')
