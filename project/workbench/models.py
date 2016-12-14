# coding=utf8

from __future__ import unicode_literals

from django.db import models


# Create your models here.
class RbacAction(models.Model):
    code = models.CharField(max_length=100, blank=False)

    class Meta:
        permissions = (
            ("op_post", "Can operate post"),  # 帖子权限
            ("op_draft_split", "Can operate draft_split"),  # 初次拆字权限
            ("op_review_split", "Can operate review_split"),  # 回查拆字权限
            ("op_final_split", "Can operate final_split"),  # 审查拆字权限
            ("op_draft_dedup", "Can operate draft_dedup"),  # 下面依照上面类推
            ("op_review_dedup", "Can operate review_dedup"),
            ("op_final_dedup", "Can operate final_dedup"),
            ("op_draft_input", "Can operate draft_input"),
            ("op_review_input", "Can operate review_input"),
            ("op_final_input", "Can operate final_input"),
            ("op_task", "Can operate task"),  # 任务操作权限
            ("op_credit", "Can operate credit"),  # 积分操作权限
            ("op_diary", "Can operate diary"),  # 日记操作权限
            ("op_gift", "Can operate gift"),  # 礼品操作权限
            ("op_forum", "Can operate forum"),  # 论坛操作权限
            ("op_user", "Can operate user"),  # 用户操作权限
            ("op_system", "Can operate system"),  # 系统操作权限
        )
