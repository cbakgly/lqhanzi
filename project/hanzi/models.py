#coding=utf-8

# Hanzi/models.py
from __future__ import unicode_literals

from django.db import models

#数据库设计中有些字段用不到，或者类型长度不合适，暂且先设成下边的
class HanziParts(models.Model):
    # id = models.AutoField(primary_key=True)       # id  主键
    # part_type = models.CharField(max_length=4, null=True, default='') #部件类型 ‘1’ ‘2’两种
    part_char = models.CharField(max_length=8, null=True, default='')  # 文字部件
    # part_pic_id = models.CharField(max_length=10, null=True, default='')  #图片部件ID
    # part_code = models.CharField(max_length=40, null=True, default='')  #部件的utf8编码
    # part_src = models.CharField(max_length=30, null=True, default='')  #部件来源
    # strokes = models.CharField(max_length=50, null=True, default='')  ##笔画数笔顺
    strokes = models.PositiveSmallIntegerField() 
    # is_using = models.CharField(max_length=1, null=True, default='') #是否启用
    stroke_order = models.CharField(max_length=20, null=True, default='')  ##笔画数笔顺    
    # remark = models.CharField(max_length=30, blank=True, default='')  #备注
    # c_t = models.DateTimeField(auto_now_add=True)  #创建时间
    # u_t = models.DateTimeField(auto_now=True)   #修改时间

    def __unicode__(self):
        # if self.part_char
        return self.part_char
        # else
        #     return self.part_pic_id
    class Meta:
        pass
        db_table='lq_hanzi_parts'
    class Admin:
        pass


class HanziSet(models.Model):
    # id = models.AutoField(primary_key=True)      
    source = models.PositiveSmallIntegerField() 
    #hanzi_type = models.PositiveSmallIntegerField() 
    hanzi_char = models.CharField(max_length=8, null=True, default='') 
    hanzi_pic_id = models.CharField(max_length=32, null=True, default='') 
    variant_type = models.PositiveSmallIntegerField()  
    std_hanzi = models.CharField(max_length=64, null=True, default='')  
    as_std_hanzi = models.CharField(max_length=32, null=True, default='') 
    seq_id = models.CharField(max_length=128, null=True, default='')
    # duplicate = models.PositiveIntegerField() 
    # duplicate_id = models.CharField(max_length=128, null=True, default='')

    dup_count = models.PositiveSmallIntegerField()
    pinyin = models.CharField(max_length=64, null=True, default='')
    radical = models.CharField(max_length=8, null=True, default='')
    strokes = models.PositiveSmallIntegerField() 
    zheng_code = models.CharField(max_length=32, null=True, default='')  
    wubi = models.CharField(max_length=32, null=True, default='') 
    structure = models.CharField(max_length=16, null=True, default='')
    # bhard = models.PositiveIntegerField()

    min_split = models.CharField(max_length=255, null=True, default='')
    deform_split = models.CharField(max_length=255, null=True, default='')
    similar_parts = models.CharField(max_length=128, null=True, default='')
    max_split = models.CharField(max_length=512, null=True, default='')
    mix_split = models.CharField(max_length=512, null=True, default='')
    stroke_serial = models.CharField(max_length=128, null=True, default='')

    remark = models.CharField(max_length=128, null=True, default='')
    #c_t = models.DateTimeField(auto_now_add=True,null=True)  #创建时间
    #u_t = models.DateTimeField(auto_now=True,null=True)   #修改时间
    inter_dict_dup_hanzi = models.CharField(max_length=64, null=True, default='')
    korean_dup_hanzi = models.CharField(max_length=32, null=True, default='')
    is_inter_dict_redundant = models.PositiveSmallIntegerField() 
    is_korean_redundant = models.PositiveSmallIntegerField() 

    def __unicode__(self):
        # if self.part_char
        return self.hanzi_char
        # else
        #     return self.part_pic_id
    class Meta:
        db_table='lq_hanzi_set'
    class Admin:
        pass



class Radical(models.Model):
    radical = models.CharField(max_length=8, null=True, default='')
    strokes = models.PositiveSmallIntegerField() 

    def __unicode__(self):
        return self.radical
    class Meta:
        db_table='lq_hanzi_radicals'
    class Admin:
        pass





