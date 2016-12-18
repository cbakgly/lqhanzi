# -*- coding:utf8 -*-
from django.shortcuts import render
from django.template import Context


def new_task_page(request):
    return render(request, 'new_task.html')


def task_package_input_list(request):
    return render(request, 'task_package_input_list.html')


def task_package_dedup_list(request):
    return render(request, 'task_package_dedup_list.html')


def task_package_split_list(request):
    return render(request, 'task_package_split_list.html')


def task_package(request):
    return render(request, 'task_package.html')
