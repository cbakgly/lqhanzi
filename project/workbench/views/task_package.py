# -*- coding:utf8 -*-
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render

from backend.cache_keys import getcachekey_today_completed_task_num
from backend.utils import get_today_credits
from backend.enums import getenum_business_status
from backend.models import TaskPackages, business_stage_choices, business_type_choices


@login_required
def new_task_page(request):
    today_credits = get_today_credits(request.user.id)
    return render(request, 'new_task.html', {"today_credits": today_credits, "business_type_choices": business_type_choices, "business_stage_choices": business_stage_choices})


@login_required
def task_package_input_list(request):
    today_credits = get_today_credits(request.user.id)
    return render(request, 'task_package_input_list.html', {"today_credits": today_credits})


@login_required
def task_package_dedup_list(request):
    today_credits = get_today_credits(request.user.id)
    return render(request, 'task_package_dedup_list.html', {"today_credits": today_credits})


@login_required
def task_package_split_list(request):
    today_credits = get_today_credits(request.user.id)
    return render(request, 'task_package_split_list.html', {"today_credits": today_credits})


@login_required
def task_package_complete(request):
    today_credits = get_today_credits(request.user.id)
    return render(request, 'task_package_complete.html', {"today_credits": today_credits})


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

    today_credits = get_today_credits(request.user.id)
    return render(request, 'task_package_ongoing.html', {'task_packages': task_packages, "today_credits": today_credits})
