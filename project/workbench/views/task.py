# -*- coding:utf8 -*-
from django.shortcuts import render


def task_split(request):
    return render(request, 'task_split.html')


def task_input(request):
    return render(request, 'task_iput.html')


def task_dedup(request):
    return render(request, 'task_dedup.html')

