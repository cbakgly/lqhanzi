# -*- coding:utf8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from backend.enums import getenum_task_package_status
from backend.models import TaskPackages, BUSINESS_STAGE_CHOICES, BUSINESS_TYPE_CHOICES
from backend.utils import get_today_complete_task_num


@login_required
def new_task_page(request):
    return render(request, 'new_task.html', {
        "business_type_choices": BUSINESS_TYPE_CHOICES,
        "business_stage_choices": BUSINESS_STAGE_CHOICES,
        "business_status_ongoing": getenum_task_package_status('ongoing')
    })


@login_required
def task_package_input_list(request):
    return render(request, 'task_package_input_list.html')


@login_required
def task_package_dedup_list(request):
    return render(request, 'task_package_dedup_list.html')


@login_required
def task_package_split_list(request):
    return render(request, 'task_package_split_list.html')


@login_required
def task_package_complete(request):
    return render(request, 'task_package_complete.html')


@login_required
def task_package_ongoing(request):
    user_id = request.user.id
    data = TaskPackages.objects.filter(user_id=user_id).filter(status=getenum_task_package_status('ongoing'))
    task_packages = []
    for counter, item in enumerate(data):
        i = item.__dict__
        i['get_business_type_display'] = item.get_business_type_display()
        i['get_business_stage_display'] = item.get_business_stage_display()
        i['today_num'] = get_today_complete_task_num(user_id, item.business_type)
        task_packages.append(i)

    return render(request, 'task_package_ongoing.html', {'task_packages': task_packages})
