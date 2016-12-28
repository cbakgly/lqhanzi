# -*- coding:utf8 -*-
from django.shortcuts import render
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from ..models import TaskPackages
from ..cache_keys import getcachekey_today_completed_task_num
from ..enums import getenum_business_status

@login_required
def new_task_page(request):
    return render(request, 'new_task.html')


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
    data = TaskPackages.objects.filter(user_id=user_id).filter(status=getenum_business_status('ongoing'))
    task_packages = []
    for counter, item in enumerate(data):
        i = item.__dict__
        i['get_business_type_display'] = item.get_business_type_display()
        i['get_business_stage_display'] = item.get_business_stage_display()
        i['today_num'] = cache.get(getcachekey_today_completed_task_num(user_id, item.business_type), 0)
        task_packages.append(i)

    return render(request, 'task_package_ongoing.html', {'task_packages': task_packages})
