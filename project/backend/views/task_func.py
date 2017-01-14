# -*- coding:utf8 -*-
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from ..models import Tasks
from ..enums import getenum_task_business_status


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
        return Response("没有更多的任务了，明天再来吧！", status=status.HTTP_204_NO_CONTENT)
