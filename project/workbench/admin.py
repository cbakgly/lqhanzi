# -*- coding:utf8 -*-
from django.contrib import admin

from models import Diaries, Credits
from models import TaskPackages, Tasks, CreditsRedeem
# Register your models here.


class DiaryAdmin(admin.ModelAdmin):
    list_display = ("user", "tag", "work_types", "work_brief", "content", "c_t", "u_t")


class CreditsAdmin(admin.ModelAdmin):
    list_display = ("user", "credit", "sort")


class TaskPackagesAdmin(admin.ModelAdmin):
    fields = ("user", "business_type", "business_stage", "size",
              "status", "daily_plan", "due_date", "completed_num", "completed_at",
              "c_t")


class TasksAdmin(admin.ModelAdmin):
    fields = ("user", "business_id", "task_package", "task_status", "credits",
              "remark", "assigned_at", "completed_at", "c_t", "business_type", "business_stage")


class CreditsRedeemAdmin(admin.ModelAdmin):
    list_display = ("applied_by", "accepted_by", "c_t", "completed_by", "accepted_at", "completed_at",
                    "reward_name", "cost_credits", "status", "remark")


admin.site.register(Diaries, DiaryAdmin)
admin.site.register(Credits, CreditsAdmin)
admin.site.register(TaskPackages, TaskPackagesAdmin)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(CreditsRedeem, CreditsRedeemAdmin)