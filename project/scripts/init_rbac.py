from backend.models import User
from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm
from backend.models import RbacAction
import traceback


# https://django-guardian.readthedocs.io/en/stable/userguide/assign.html

def run():
    try:
        try:
            action = RbacAction.objects.get(code='op')
        except:
            action = RbacAction.objects.create(code='op')

        group = Group.objects.create(name='grp_draft_split')
        assign_perm("op_draft_split", group, action)
        assign_perm("op_forum", group, action)
        group = Group.objects.create(name='grp_review_split')
        assign_perm("op_review_split", group, action)
        assign_perm("op_forum", group, action)
        group = Group.objects.create(name='grp_final_split')
        assign_perm("op_final_split", group, action)
        assign_perm("op_forum", group, action)
        group = Group.objects.create(name='grp_draft_dedup')
        assign_perm("op_draft_dedup", group, action)
        assign_perm("op_forum", group, action)
        group = Group.objects.create(name='grp_review_dedup')
        assign_perm("op_review_dedup", group, action)
        assign_perm("op_forum", group, action)
        group = Group.objects.create(name='grp_final_dedup')
        assign_perm("op_final_dedup", group, action)
        assign_perm("op_forum", group, action)
        group = Group.objects.create(name='grp_draft_input')
        assign_perm("op_draft_input", group, action)
        assign_perm("op_forum", group, action)
        group = Group.objects.create(name='grp_review_input')
        assign_perm("op_review_input", group, action)
        assign_perm("op_forum", group, action)
        group = Group.objects.create(name='grp_final_input')
        assign_perm("op_final_input", group, action)
        assign_perm("op_forum", group, action)
        group = Group.objects.create(name='grp_volunteer')
        assign_perm("op_forum", group, action)

        group = Group.objects.create(name='grp_forum_admin')
        assign_perm("op_forum", group, action)

        admin = User.objects.create_user('forum_admin', password='forum_admin')
        admin.groups.add(group)

        group = Group.objects.create(name='grp_task_admin')
        assign_perm("op_task", group, action)

        admin = User.objects.create_user('task_admin', password='task_admin')
        admin.groups.add(group)

        group = Group.objects.create(name='grp_gift_admin')
        assign_perm("op_gift", group, action)

        admin = User.objects.create_user('gift_admin', password='gift_admin')
        admin.groups.add(group)

        group = Group.objects.create(name='grp_sys_admin')
        assign_perm("op_system", group, action)

        admin = User.objects.create_user('sys_admin', password='sys_admin')
        admin.groups.add(group)

        group = Group.objects.create(name='grp_user_admin')
        assign_perm("op_user", group, action)

        admin = User.objects.create_user('user_admin', password='user_admin')
        admin.groups.add(group)

    except:
        traceback.print_exc()
