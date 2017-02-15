# -*- coding:utf8 -*-
from django.contrib import admin
from django.contrib.auth.models import Permission
from backend.models import *


class DiaryAdmin(admin.ModelAdmin):
    list_display = ("user", "tag", "work_types", "work_brief", "content", "c_t", "u_t")


class CreditsAdmin(admin.ModelAdmin):
    list_display = ("user", "credit", "sort")


class TaskPackagesAdmin(admin.ModelAdmin):
    fields = (
        "user", "business_type", "business_stage", "size",
        "status", "daily_plan", "due_date", "completed_num", "completed_at",
        "c_t"
    )


class KoreanDupChaAdmin(admin.ModelAdmin):
    fields = ("korean_variant", "unicode")


# class TasksInline(admin.TabularInline):
#     model = Tasks


class TasksAdmin(admin.ModelAdmin):
    fields = ("user",
              "task_package",
              "business_type",
              "business_stage",
              "task_status",
              "credits",
              "remark",
              "assigned_at",
              "completed_at",
              "c_t",
              "content_type",
              "object_id",
              )


class VariantsSplitAdmin(admin.ModelAdmin):
    fieldsets = [
        ('基础信息', {
            'fields':
                [
                    'source',
                    'hanzi_type',
                    'hanzi_char',
                    'hanzi_pic_id',
                    'variant_type',
                    'std_hanzi',
                    'as_std_hanzi',
                    'seq_id',
                    'is_redundant',
                ]
        }),
        ('初次', {
            'fields':
                [
                    'skip_num_draft',
                    'init_split_draft',
                    'other_init_split_draft',
                    'deform_split_draft',
                    'similar_parts_draft',
                    'dup_id_draft',
                ]
        }),
        ('回查', {
            'fields':
                [
                    'skip_num_review',
                    'init_split_review',
                    'other_init_split_review',
                    'deform_split_review',
                    'similar_parts_review',
                    'dup_id_review',
                ]
        }),
        ('审查', {
            'fields':
                [
                    'skip_num_final',
                    'init_split_final',
                    'other_init_split_final',
                    'deform_split_final',
                    'similar_parts_final',
                    'dup_id_final',
                ]
        }),
        ('比较', {
            'fields':
                [
                    'is_draft_equals_review',
                    'is_review_equals_final',
                    'is_checked',
                    'is_submitted',
                    'remark',
                ]
        }),
    ]


class CreditRedeemInline(admin.TabularInline):
    model = CreditsRedeem


# class RewardAdmin(admin.ModelAdmin):
# inlines = [CreditRedeemInline]


class CreditsRedeemAdmin(admin.ModelAdmin):
    list_display = (
        "applied_by", "accepted_by", "c_t", "completed_by", "accepted_at", "completed_at",
        "reward_name", "cost_credits", "status", "remark"
    )


class InputPageAdmin(admin.ModelAdmin):
    list_display = ('page_num',)


class VariantsInputAdmin(admin.ModelAdmin):
    model = VariantsInput


class TaskTypeAdmin(admin.ModelAdmin):
    model = TaskTypes


class KoreanVariantsDictAdmin(admin.ModelAdmin):
    model = KoreanVariantsDict


class HanziRadicalsAdmin(admin.ModelAdmin):
    model = HanziRadicals


class KoreanDupZhengCodesAdmin(admin.ModelAdmin):
    model = KoreanDupZhengCodes


class KoreanDedupAdmin(admin.ModelAdmin):
    model = KoreanDedup


class InterDictDedupAdmin(admin.ModelAdmin):
    model = InterDictDedup


class RewardAdmin(admin.ModelAdmin):
    model = Reward


class HanziPartsAdmin(admin.ModelAdmin):
    model = HanziParts


class UserTaskProfileAdmin(admin.ModelAdmin):
    model = UserTaskProfile


admin.site.register(User)
admin.site.register(Permission)
admin.site.register(HanziSet)
admin.site.register(TaskPackages, TaskPackagesAdmin)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(TaskTypes, TaskTypeAdmin)
admin.site.register(InputPage, InputPageAdmin)
admin.site.register(VariantsSplit, VariantsSplitAdmin)
admin.site.register(VariantsInput, VariantsInputAdmin)
admin.site.register(KoreanVariantsDict, KoreanVariantsDictAdmin)
admin.site.register(HanziRadicals, HanziRadicalsAdmin)
admin.site.register(KoreanDupCharacters, KoreanDupChaAdmin)
admin.site.register(KoreanDupZhengCodes, KoreanDupZhengCodesAdmin)
admin.site.register(KoreanDedup, KoreanDedupAdmin)
admin.site.register(InterDictDedup, InterDictDedupAdmin)
admin.site.register(Reward, RewardAdmin)
admin.site.register(CreditsRedeem, CreditsRedeemAdmin)
admin.site.register(Diaries, DiaryAdmin)
admin.site.register(Credits, CreditsAdmin)
admin.site.register(HanziParts, HanziPartsAdmin)
admin.site.register(UserTaskProfile, UserTaskProfileAdmin)
