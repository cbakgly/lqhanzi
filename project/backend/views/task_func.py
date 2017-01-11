# -*- coding:utf8 -*-
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from ..models import Tasks


# 分配新任务
def assign_task(business_type, business_stage, task_package, user):
    tasks = list(Tasks.objects.filter(business_type=business_type).filter(assigned_at=None).filter(business_stage=business_stage).filter(task_status=1))
    if len(tasks):
        task = tasks[0]
        task.user = user
        task.task_package = task_package
        task.task_status = 2
        # task.credits = list(TaskCredit.objects.filter(business_type=business_type).filter(business_stage=business_stage))[0].business_credit
        task.credits = 2
        task.assigned_at = timezone.now()
        task.save()
        return task
    else:
        return Response("没有更多的任务了，明天再来吧！", status=status.HTTP_204_NO_CONTENT)
