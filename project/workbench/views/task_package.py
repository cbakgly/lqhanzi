# -*- coding:utf8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from backend.enums import getenum_task_package_status
from backend.models import TaskPackages
from backend.utils import get_today_complete_task_num


@login_required
def new_task_page(request):
    return render(request, 'new_task.html')


@login_required
def task_package_input_list(request, *args, **kwargs):
    return render(request, 'task_package_input_list.html', kwargs)


@login_required
def task_package_dedup_list(request, *args, **kwargs):
    return render(request, 'task_package_dedup_list.html', kwargs)


@login_required
def task_package_split_list(request, *args, **kwargs):
    return render(request, 'task_package_split_list.html', kwargs)


@login_required
def task_package_complete(request):
    return render(request, 'task_package_complete.html')


@login_required
def task_package_ongoing(request):
    user = request.user
    data = TaskPackages.objects.filter(user_id=user.id, status=getenum_task_package_status('ongoing'))
    task_packages = []
    for counter, item in enumerate(data):
        i = item.__dict__
        i['get_business_type_display'] = item.get_business_type_display()
        i['get_business_stage_display'] = item.get_business_stage_display()
        i['today_num'] = get_today_complete_task_num(user.id, item.business_type)
        i['get_status_display'] = item.get_status_display()
        task_packages.append(i)

    return render(request, 'task_package_ongoing.html', {
        'task_packages': task_packages,
    })
