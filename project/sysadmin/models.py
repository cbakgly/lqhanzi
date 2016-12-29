# -*- coding:utf8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
from guardian.mixins import GuardianUserMixin


class User(AbstractUser, GuardianUserMixin):
    gender_choices = ((0, 'M'), (1, 'F'))
    gender = models.IntegerField(u'性别', choices=gender_choices, default=0)
    mb = models.CharField(u'手机号', max_length=32, blank=True, null=True)
    qq = models.CharField(u'腾讯QQ', max_length=32, blank=True, null=True)
    address = models.CharField(u'地址', max_length=64, blank=True, null=True)
    avatar = models.FileField(u'头像', null=True)
    u_t = models.DateTimeField(u'修改时间', blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'user'


# Operation log table
class Operation(models.Model):
    logtype_choices = (
        (0, u'常规日志'),
        (1, u'任务包管理'),
        (2, u'任务管理'),
        (3, u'奖品管理'),
        (4, u'讨论区管理'),
        (5, u'用户管理'),
    )
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    logtype = models.IntegerField(u'日志类型', choices=logtype_choices, default=0)
    message = models.CharField(u'日志内容', max_length=1024)
    logtime = models.DateTimeField(u'记录时间', auto_now=True)

    def __unicode__(self):
        return self.message

    class Meta:
        db_table = 'operation_log'


class RbacAction(models.Model):
    code = models.CharField(max_length=100, blank=False)

    class Meta:
        permissions = (
            # 帖子权限
            ("op_post", "Can operate post"),
            # 初次拆字权限
            ("op_draft_split", "Can operate draft_split"),
            # 回查拆字权限
            ("op_review_split", "Can operate review_split"),
            # 审查拆字权限
            ("op_final_split", "Can operate final_split"),
            # 下面依照上面类推
            ("op_draft_dedup", "Can operate draft_dedup"),
            ("op_review_dedup", "Can operate review_dedup"),
            ("op_final_dedup", "Can operate final_dedup"),
            ("op_draft_input", "Can operate draft_input"),
            ("op_review_input", "Can operate review_input"),
            ("op_final_input", "Can operate final_input"),
            # 任务操作权限
            ("op_task", "Can operate task"),
            # 积分操作权限
            ("op_credit", "Can operate credit"),
            # 日记操作权限
            ("op_diary", "Can operate diary"),
            # 礼品操作权限
            ("op_gift", "Can operate gift"),
            # 论坛操作权限
            ("op_forum", "Can operate forum"),
            # 用户操作权限
            ("op_user", "Can operate user"),
            # 系统操作权限
            ("op_system", "Can operate system"),
        )
        db_table = 'rbac_actions'
