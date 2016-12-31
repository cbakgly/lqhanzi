# -*- coding:utf8 -*-
from django.contrib import admin

from models import Diaries, Credits, VariantsSplit
# VariantsInput, KoreanDedup, InterDictDedup
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


class TasksInline(admin.TabularInline):
    model = Tasks


class TasksAdmin(admin.ModelAdmin):
    fields = ("user",
              "variant_split",
              "variant_input",
              "korean_dedup",
              "interdict_dedup",
              "task_package",
              "business_type",
              "business_stage",
              "task_status",
              "credits",
              "remark",
              "assigned_at",
              "completed_at",
              "c_t"
              )


class VariantsSplitAdmin(admin.ModelAdmin):
    inlines = [TasksInline]
    fieldsets = (
        ['Main', {
            'fields': ("source", "hanzi_type", "hanzi_char"),
        }],
    ['Advance', {
        'classes': ('collapse',),
        'fields': ("skip_num_draft", "init_split_draft", "other_init_split_draft"),
    }]
    )


class CreditsRedeemAdmin(admin.ModelAdmin):
    list_display = ("applied_by", "accepted_by", "c_t", "completed_by", "accepted_at", "completed_at",
                    "reward_name", "cost_credits", "status", "remark")


admin.site.register(Diaries, DiaryAdmin)
admin.site.register(Credits, CreditsAdmin)
admin.site.register(TaskPackages, TaskPackagesAdmin)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(VariantsSplit, VariantsSplitAdmin)
admin.site.register(CreditsRedeem, CreditsRedeemAdmin)
