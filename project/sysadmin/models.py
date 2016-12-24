# -*- coding:utf8 -*-
# encoding: utf-8
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from guardian.mixins import GuardianUserMixin


class User(AbstractUser, GuardianUserMixin):
    gender_choices = ((0, 'M'), (1, 'F'))
    gender = models.IntegerField(u'性别', choices=gender_choices, default=0)
    mb = models.CharField(u'手机号', max_length=32, blank=True)
    qq = models.CharField(u'腾讯QQ', max_length=32, blank=True)
    address = models.CharField(u'地址', max_length=64, blank=True)
    avatar = models.FileField(u'头像')
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)

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
