# -*- coding:utf8 -*-

from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone


# Create your models here.

class HanziSet(models.Model):
    source = models.SmallIntegerField(u'来源', null=True)
    hanzi_type = models.SmallIntegerField(u'字形类型：文字、图片、文字且图片', null=True)
    hanzi_char = models.CharField(u'文字', null=True, max_length=8)
    hanzi_pic_id = models.CharField(u'图片字编码', null=True, max_length=32)
    variant_type = models.SmallIntegerField(u'正异类型', null=True)
    std_hanzi = models.CharField(u'所属正字', null=True, max_length=64)
    as_std_hanzi = models.CharField(u'兼正字号', null=True, max_length=32)
    seq_id = models.CharField(u'字的位置统一编码', null=True, max_length=32)
    pinyin = models.CharField(u'拼音', null=True, max_length=64)
    radical = models.CharField(u'部首', null=True, max_length=8)
    strokes = models.SmallIntegerField(u'笔画数', null=True)
    zheng_code = models.CharField(u'郑码', null=True, max_length=32)
    wubi = models.CharField(u'五笔', null=True, max_length=32)
    is_redundant = models.SmallIntegerField(u'是否多余', null=True)
    dup_count = models.SmallIntegerField(u'重复次数', null=True)
    inter_dict_dup_hanzi = models.CharField(u'异体字字典间重复编码', null=True, max_length=64)
    korean_dup_hanzi = models.CharField(u'高丽异体字字典内部重复编码', null=True, max_length=32)
    structure = models.CharField(u'结构', null=True, max_length=16)
    skip_num = models.SmallIntegerField(u'跳过次数，多的话算难字', null=True)
    min_split = models.CharField(u'跳过次数，多的话算难字', max_length=255, null=True)
    max_split = models.CharField(u'最大拆分', max_length=512, null=True)
    mix_split = models.CharField(u'混合拆分', max_length=512, null=True)
    deform_split = models.CharField(u'调笔拆分', max_length=255, null=True)
    similar_parts = models.CharField(u'相似部件', max_length=128, null=True)
    stroke_serial = models.CharField(u'部件序列', max_length=128, null=True)
    remark = models.CharField(u'备注', max_length=128, null=True)
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)

    class Meta:
        db_table = 'hanzi_set'
