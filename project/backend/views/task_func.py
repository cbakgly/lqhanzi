# -*- coding:utf8 -*-
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from ..models import Tasks, TaskPackages, VariantsInput, UserTaskProfile
from ..enums import getenum_task_status, getenum_business_type, getenum_business_stage


def get_user_task_profile(user):
    profile = UserTaskProfile.objects.filter(user=user).first()
    if not profile:
        profile = UserTaskProfile(user=user)
        profile.save()
    return profile


def convert_profile_to_dict(profile):
    return {"id": profile.id,
            getenum_business_type('split'): profile.last_split_id,
            getenum_business_type('dedup'): profile.last_dedup_id,
            getenum_business_type('input_page'): profile.last_input_id
            }


def update_user_task_profile(**kwargs):
    user = kwargs['user']
    task_id = kwargs['task_id']
    business_type = kwargs['business_type']

    profile = get_user_task_profile(user)
    if business_type == getenum_business_type('split'):
        profile.last_split_id = task_id
    elif business_type == getenum_business_type('dedup'):
        profile.last_dedup_id = task_id
    else:
        profile.last_input_id = task_id
    profile.save()
    return profile


def reset_task(task):
    task.task_package = None
    task.assigned_at = None
    task.user = None
    task.task_status = getenum_task_status('to_be_arranged')
    task.save()

    return task


def get_working_task(task_package, user):
    task = Tasks.objects.filter(user=user).filter(task_package=task_package).filter(task_status=getenum_task_status('ongoing'))
    if task:
        return task[0]
    return {}


# 分配新任务
def assign_task(business_type, business_stage, task_package, user):
    profile = convert_profile_to_dict(get_user_task_profile(user))

    task = Tasks.objects.filter(business_type=business_type)\
                        .filter(business_stage=business_stage)\
                        .filter(task_status=getenum_task_status("to_be_arranged"))\
                        .filter(id__gt=profile[business_type]).first()
    if task:
        task.user = user
        task.task_package = task_package
        task.task_status = getenum_task_status("ongoing")
        task.credits = 0 if business_type in [getenum_business_type("input_page"), getenum_business_type("dedup")] else 2
        task.assigned_at = timezone.now()
        task.save()
        update_user_task_profile(user=user, business_type=business_type, task_id=task.id)
        return task
    return {}


def assign_task_by_task_ele(task_ele, business_stage, task_package, user):
    page_num = task_ele.page_num
    if business_stage is getenum_business_stage('init'):
        seq_num = task_ele.seq_num_draft
        seq_order = 'seq_num_draft'
    elif business_stage is getenum_business_stage('review'):
        seq_num = task_ele.seq_num_review
        seq_order = 'seq_num_review'
    else:
        seq_num = task_ele.seq_num_final
        seq_order = 'seq_num_final'

    inputs = list(VariantsInput.objects.filter(page_num=page_num, seq_num_draft__gt=seq_num).order_by(seq_order))

    if inputs:
        tasks = list(inputs[0].task.all())
        task_dict = {}

        for t in tasks:
            task_dict[t.business_stage] = t
        task_to_assign = task_dict[business_stage]
        task_to_assign.user = user
        task_to_assign.task_package = task_package
        task_to_assign.task_status = getenum_task_status("ongoing")
        task_to_assign.save()


def assign_task_by_page(business_stage, task_package, user):
    init_stage = getenum_business_stage('init')
    review_stage = getenum_business_stage('review')

    latest_task = list(Tasks.objects.filter(business_type=getenum_business_type('input'), task_status=getenum_task_status("ongoing")).order_by('id'))[-1]
    page_num = latest_task.task_ele.page_num
    if business_stage is init_stage:
        seq_order = 'seq_num_draft'
    elif business_stage is review_stage:
        seq_order = 'seq_num_review'
    else:
        seq_order = 'seq_num_final'

    inputs = list(VariantsInput.objects.filter(page_num=page_num + 1).order_by(seq_order))[0]

    if inputs:
        tasks = list(inputs[0].task.all())
        task_dict = {}
        for t in tasks:
            task_dict[t.business_stage] = t
        task_to_assign = task_dict[business_stage]
        if business_stage is init_stage:
            task_to_assign.user = user
            task_to_assign.task_package = task_package
            task_to_assign.task_status = getenum_task_status("ongoing")
            task_to_assign.save()
            return task_to_assign
        else:
            if task_to_assign.task_status is getenum_task_status("closed"):
                return None
            else:
                task_to_assign.user = user
                task_to_assign.task_package = task_package
                task_to_assign.task_status = getenum_task_status("ongoing")
                task_to_assign.save()
                return task_to_assign
    else:
        pass


# 用于给去重分配后生成任务
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
            'business_type': getenum_business_type('dedup_child'),
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


def has_task(task_ele, business_stage):
    tasks = list(Tasks.objects.filter(object_id=task_ele.id, business_stage=business_stage))
    return tasks


def task_to_arrange(business_type, business_stage):
    task = Tasks.objects.filter(business_type=business_type) \
        .filter(business_stage=business_stage) \
        .filter(task_status=getenum_task_status("to_be_arranged")).first()
    if task:
        return True
    else:
        return False

def get_stage(task_package_id):
    return list(TaskPackages.objects.filter(id=task_package_id))[0].business_stage
