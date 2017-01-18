# -*- coding:utf8 -*-
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from ..models import Tasks, TaskPackages
from ..enums import getenum_task_business_status
from django.contrib.contenttypes.models import ContentType


# 分配新任务
def assign_task(business_type, business_stage, task_package, user):
    tasks = list(Tasks.objects.filter(business_type=business_type).filter(business_stage=business_stage).filter(task_status=getenum_task_business_status("to_be_arranged")))
    if len(tasks):
        task = tasks[0]
        task.user = user
        task.task_package = task_package
        task.task_status = getenum_task_business_status("ongoing")
        # task.credits = list(TaskCredit.objects.filter(business_type=business_type).filter(business_stage=business_stage))[0].business_credit
        task.credits = 2
        task.assigned_at = timezone.now()
        task.save()
        return task
    else:
        return Response(_("No more task today, have a try tommorrow!"), status=status.HTTP_204_NO_CONTENT)


def assign_input_task(business_type, business_stage, task_package, user):
    tasks = Tasks.objects.filter(business_type=business_type).filter(business_stage=business_stage).filter(task_status=getenum_task_business_status("to_be_arranged"))
    if len(tasks):
        task = tasks[0]
        page_num = task.task_ele.page_num
        return page_num


def create_task(new_task_data):
    task_package = list(TaskPackages.objects.filter(pk=new_task_data['task_package']))[0]
    content_object = new_task_data['content']
    business_stage = task_package.business_stage
    tasks = list(content_object.task.all())
    stages = [t.business_stage for t in tasks]
    if business_stage not in stages:
        data = {
            'user': new_task_data['user'],
            'task_package': task_package,
            'task_status': 3,
            'business_type': 1000,
            'business_stage': task_package.business_stage,
            'credits': 2,
            'remark': "",
            'assigned_at': timezone.now(),
            'completed_at': timezone.now(),
            'c_t': timezone.now(),
            'u_t': timezone.now(),
            'content_type': list(ContentType.objects.filter(model="interdictdedup", app_label="backend"))[0],
            'object_id': content_object.id
        }

        new_task = Tasks(user=data["user"])
        for key in data.keys():
            setattr(new_task, key, data.get(key, getattr(new_task, key)))
        new_task.save()
        return business_stage
    else:
        return business_stage
