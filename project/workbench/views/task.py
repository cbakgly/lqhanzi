# -*- coding:utf8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def task_split(request):
    return render(request, 'task_split.html')


@login_required
def task_input(request):
    return render(request, 'task_iput.html')


@login_required
def task_dedup(request):
    return render(request, 'task_dedup.html')

