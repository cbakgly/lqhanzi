#coding=utf-8

# Hanzi/models.py
from __future__ import unicode_literals
from django.db import models

class HanziParts(models.Model):
    part_char = models.CharField(max_length=8, null=True, default='')  # 文字部件
    strokes = models.PositiveSmallIntegerField() 
    stroke_order = models.CharField(max_length=20, null=True, default='')  #笔画数笔顺    

    def __unicode__(self):
        return self.part_char

    class Meta:
        pass
        db_table='lq_hanzi_parts'


class HanziSet(models.Model): 
    source = models.PositiveSmallIntegerField() 
    hanzi_char = models.CharField(max_length=8, null=True, default='') 
    hanzi_pic_id = models.CharField(max_length=32, null=True, default='') 
    variant_type = models.PositiveSmallIntegerField()  
    std_hanzi = models.CharField(max_length=64, null=True, default='')  
    as_std_hanzi = models.CharField(max_length=32, null=True, default='') 
    seq_id = models.CharField(max_length=128, null=True, default='')

    dup_count = models.PositiveSmallIntegerField()
    pinyin = models.CharField(max_length=64, null=True, default='')
    radical = models.CharField(max_length=8, null=True, default='')
    strokes = models.PositiveSmallIntegerField() 
    zheng_code = models.CharField(max_length=32, null=True, default='')  
    wubi = models.CharField(max_length=32, null=True, default='') 
    structure = models.CharField(max_length=16, null=True, default='')

    min_split = models.CharField(max_length=255, null=True, default='')
    deform_split = models.CharField(max_length=255, null=True, default='')
    similar_parts = models.CharField(max_length=128, null=True, default='')
    max_split = models.CharField(max_length=512, null=True, default='')
    mix_split = models.CharField(max_length=512, null=True, default='')
    stroke_serial = models.CharField(max_length=128, null=True, default='')

    remark = models.CharField(max_length=128, null=True, default='')
    inter_dict_dup_hanzi = models.CharField(max_length=64, null=True, default='')
    korean_dup_hanzi = models.CharField(max_length=32, null=True, default='')
    is_inter_dict_redundant = models.PositiveSmallIntegerField() 
    is_korean_redundant = models.PositiveSmallIntegerField() 

    def __unicode__(self):
        if self.part_char:
            return self.hanzi_char
        else:
            return self.part_pic_id
    class Meta:
        db_table='lq_hanzi_set'



class Radical(models.Model):
    radical = models.CharField(max_length=8, null=True, default='')
    strokes = models.PositiveSmallIntegerField() 

    def __unicode__(self):
        return self.radical
    class Meta:
        db_table='lq_hanzi_radicals'






