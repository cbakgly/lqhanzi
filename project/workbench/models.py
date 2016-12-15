# -*- coding:utf8 -*-
from __future__ import unicode_literals

from django.db import models
from sysadmin.models import User
import datetime


# Create your models here.
class Tag(models.Model):
    """
    打卡标签
    """
    tag = models.CharField(max_length=16)

    def __unicode__(self):
        return self.tag


class Diary(models.Model):
    """打卡"""
    user_id = models.IntegerField()
    tag = models.ForeignKey(Tag)
    work_types = models.CharField(max_length=16, default="拆字")
    work_brief = models.CharField(max_length=64, default="打卡")
    content = models.TextField(default="愿此殊胜功德，回向法界有情，尽除一切罪障，共成无上菩提！")
    c_t = models.DateTimeField()
    u_t = models.DateTimeField()

    def __Unicode__(self):
        return self.writer.username


