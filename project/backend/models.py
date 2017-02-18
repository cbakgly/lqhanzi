# -*- coding:utf8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

VARIANT_TYPE_CHOICES = ((0, u'纯正字'), (1, u'狭义异体字'), (2, u'广义且正字'), (3, u'广义异体字'), (4, u'狭义且正字'), (5, u'特定异体字'), (6, u'特定且正字'), (7, u'误刻误印'), (8, u'其他不入库类型'), (9, u'其他入库类型'))
INPUT_VARIANT_TYPE_CHOICES = ((1, u'狭义异体字'), (2, u'简化字'), (3, u'类推简化字'), (4, u'讹字'), (5, u'古今字'), (6, '@'))
HANZI_TYPE_CHOICES = ((0, u'文字'), (1, u'图片'), (2, u'文字且图片'))
SOURCE_CHOICES = ((0, u'未分类'), (1, 'Unicode'), (2, u'台湾异体字典'), (3, u'汉语大字典'), (4, u'高丽大藏经'), (5, u'敦煌俗字典'))
YESNO_CHOICES = ((0, u'否'), (1, u'是'))
BUSINESS_TYPE_CHOICES = ((1, u'拆字'), (2, u'录入'), (3, u'图书校对'), (4, u'论文下载'), (5, u'去重'), (6, u'高台拆字'), (7, u'互助'), (8, u'去重子任务'))
BUSINESS_STAGE_CHOICES = ((1, u'初次'), (2, u'回查'), (3, u'审查'))
TASK_PACKAGE_STATUS_CHOICES = ((0, u'进行中'), (1, u'已完成'))
TASK_STATUS_CHOICES = ((0, u'未开放'), (1, u'待分配'), (2, u'进行中'), (3, u'已完成'))
SUPERUSER_ENUM = ((0, u'普通用户'), (1, u'超级管理员'))
ISACTIVE = ((0, 'inactive'), (1, 'active'))


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    gender_choices = ((0, 'Male'), (1, 'Female'))
    gender = models.IntegerField(u'性别', choices=gender_choices, default=0)
    mb = models.CharField(u'手机号', max_length=32, blank=True, default='')
    qq = models.CharField(u'腾讯QQ', max_length=32, blank=True, default='')
    address = models.CharField(u'地址', max_length=64, blank=True, default='')
    avatar = models.FileField(u'头像', blank=True, null=True)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)

    class Meta:
        db_table = 'user'
        verbose_name_plural = u"用户记录"
        verbose_name = u"用户记录"

    def __unicode__(self):
        return SUPERUSER_ENUM[self.is_superuser][1] + ':' + ISACTIVE[self.is_active][1] + ':' + self.username + ':' + self.email


class HanziSet(models.Model):
    source = models.SmallIntegerField(u'来源', choices=SOURCE_CHOICES, default=0)
    hanzi_type = models.SmallIntegerField(u'字形类型：文字、图片、文字且图片', choices=HANZI_TYPE_CHOICES, default=0)
    hanzi_char = models.CharField(u'文字', default='', blank=True, max_length=8, db_index=True)
    hanzi_pic_id = models.CharField(u'图片字编码', default='', blank=True, max_length=32)

    variant_type = models.SmallIntegerField(u'正异类型', choices=VARIANT_TYPE_CHOICES, null=True)
    std_hanzi = models.CharField(u'所属正字', default='', blank=True, max_length=64)
    as_std_hanzi = models.CharField(u'兼正字号', default='', blank=True, max_length=32)
    seq_id = models.CharField(u'字的位置统一编码', default='', blank=True, max_length=32)

    pinyin = models.CharField(u'拼音', default='', blank=True, max_length=64)
    radical = models.CharField(u'部首', default='', blank=True, max_length=8)
    max_strokes = models.SmallIntegerField(u'最大笔画数', default='', blank=True)
    min_strokes = models.SmallIntegerField(u'最小笔画数', default='', blank=True)

    zheng_code = models.CharField(u'郑码', default='', blank=True, max_length=32)
    wubi = models.CharField(u'五笔', default='', blank=True, max_length=32)

    dup_count = models.SmallIntegerField(u'重复次数', default=0)
    inter_dict_dup_hanzi = models.CharField(u'异体字字典间重复编码', default='', blank=True, max_length=64)
    korean_dup_hanzi = models.CharField(u'高丽异体字字典内部重复编码', default='', blank=True, max_length=32)
    is_korean_redundant = models.BooleanField(u'是否多余高丽异体字', choices=YESNO_CHOICES, default=False)
    is_inter_dict_redundant = models.BooleanField(u'是否多余台湾高丽异体字', choices=YESNO_CHOICES, default=False)

    structure = models.CharField(u'结构', max_length=16, default='', blank=True)
    min_split = models.CharField(u'初步拆分', max_length=255, default='', blank=True)
    max_split = models.CharField(u'最大拆分', max_length=512, default='', blank=True)
    mix_split = models.CharField(u'混合拆分', max_length=512, default='', blank=True)
    deform_split = models.CharField(u'调笔拆分', max_length=255, default='', blank=True)
    similar_parts = models.CharField(u'相似部件', max_length=128, default='', blank=True)
    stroke_serial = models.CharField(u'部件序列', max_length=128, default='', blank=True)

    remark = models.CharField(u'备注', max_length=128, default='', blank=True)
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)

    class Meta:
        db_table = 'lq_hanzi_set'
        verbose_name = u"汉字"
        verbose_name_plural = u"汉字"

    def __unicode__(self):
        return self.hanzi_char + ':' + self.hanzi_pic_id


class TaskPackages(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, null=True, related_name="user_tps")  # 用户，拆字员
    business_type = models.SmallIntegerField(u'任务类型', choices=BUSINESS_TYPE_CHOICES, null=True)
    business_stage = models.SmallIntegerField(u'任务阶段', choices=BUSINESS_STAGE_CHOICES, null=True)
    size = models.SmallIntegerField(u'工作包大小', null=False, default=100)
    status = models.SmallIntegerField(u'工作包状态', choices=TASK_PACKAGE_STATUS_CHOICES, default=0)
    daily_plan = models.SmallIntegerField(u'日计划工作量', null=False, default=5)
    due_date = models.DateTimeField(u'预计完成时间', null=True)
    completed_num = models.SmallIntegerField(u'已完成数量', default=0)
    completed_at = models.DateTimeField(u'完成时间', null=True)
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)

    class Meta:
        db_table = 'lq_task_packages'
        verbose_name = u"任务包"
        verbose_name_plural = u"任务包"

    def __unicode__(self):
        return "#" + BUSINESS_TYPE_CHOICES[self.business_type - 1][1] + BUSINESS_STAGE_CHOICES[self.business_stage - 1][
            1] + str(self.size) + str(self.id)


class TaskTypes(models.Model):
    business_type = models.SmallIntegerField(u'任务类型', choices=BUSINESS_TYPE_CHOICES, null=True)
    business_name = models.CharField(u'任务名称', max_length=64, default='', blank=True)
    credits = models.SmallIntegerField(u'单个任务积分', default=0)
    is_active = models.BooleanField(u'是否启用', default=True)

    class Meta:
        db_table = 'lq_task_types'
        verbose_name = u"任务类型积分"
        verbose_name_plural = u"任务类型积分"


class Tasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_task")  # 用户，拆字员
    task_package = models.ForeignKey(TaskPackages, related_name='tasks', on_delete=models.SET_NULL, null=True)

    object_id = models.PositiveIntegerField(null=True)
    business_id = models.IntegerField(u'业务ID，指的是对应于拆字、去重、录入业务表的ID', null=True)
    business_type = models.SmallIntegerField(u'任务类型', choices=BUSINESS_TYPE_CHOICES, null=True)
    business_stage = models.SmallIntegerField(u'任务阶段', choices=BUSINESS_STAGE_CHOICES, null=True)
    task_status = models.SmallIntegerField(u'任务状态', choices=TASK_STATUS_CHOICES, null=True)

    credits = models.SmallIntegerField(u'积分', default=0)
    remark = models.CharField(u'备注', max_length=128, default='', blank=True)

    assigned_at = models.DateTimeField(u'分配时间', null=True)
    completed_at = models.DateTimeField(u'完成时间', null=True)
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'lq_tasks'
        ordering = ['id']
        verbose_name = u"任务"
        verbose_name_plural = u"任务"

    def __unicode__(self):
        return "#" + BUSINESS_TYPE_CHOICES[self.business_type - 1][1] + BUSINESS_STAGE_CHOICES[self.business_stage - 1][
            1] + str(self.id)


class VariantsSplit(models.Model):
    source = models.SmallIntegerField(u'来源', choices=SOURCE_CHOICES, default=0)
    hanzi_type = models.SmallIntegerField(u'字形类型：文字、图片、文字且图片', choices=HANZI_TYPE_CHOICES, default=0)
    hanzi_char = models.CharField(u'文字', default='', blank=True, max_length=8)
    hanzi_pic_id = models.CharField(u'图片字编码', default='', blank=True, max_length=32)

    variant_type = models.SmallIntegerField(u'正异类型', choices=VARIANT_TYPE_CHOICES, null=True)
    std_hanzi = models.CharField(u'所属正字', default='', blank=True, max_length=64)
    as_std_hanzi = models.CharField(u'兼正字号', default='', blank=True, max_length=32)
    seq_id = models.CharField(u'字的位置统一编码', default='', blank=True, max_length=32)
    is_redundant = models.BooleanField(u'是否多余', choices=YESNO_CHOICES, default=False)

    skip_num_draft = models.SmallIntegerField(u'太难跳过次数', default=0)
    init_split_draft = models.CharField(u'初步拆分', max_length=128, default='', blank=True)
    other_init_split_draft = models.CharField(u'其它初步拆分', max_length=128, default='', blank=True)
    deform_split_draft = models.CharField(u'调笔拆分', max_length=128, default='', blank=True)
    similar_parts_draft = models.CharField(u'相似部件', max_length=64, default='', blank=True)
    dup_id_draft = models.CharField(u'重复ID', max_length=32, default='', blank=True)

    skip_num_review = models.SmallIntegerField(u'太难跳过次数', default=0)
    init_split_review = models.CharField(u'初步拆分', max_length=128, default='', blank=True)
    other_init_split_review = models.CharField(u'其它初步拆分', max_length=128, default='', blank=True)
    deform_split_review = models.CharField(u'调笔拆分', max_length=128, default='', blank=True)
    similar_parts_review = models.CharField(u'相似部件', max_length=64, default='', blank=True)
    dup_id_review = models.CharField(u'重复ID', max_length=32, default='', blank=True)

    skip_num_final = models.SmallIntegerField(u'太难跳过次数', default=0)
    init_split_final = models.CharField(u'初步拆分', max_length=128, default='', blank=True)
    other_init_split_final = models.CharField(u'其它初步拆分', max_length=128, default='', blank=True)
    deform_split_final = models.CharField(u'调笔拆分', max_length=128, default='', blank=True)
    similar_parts_final = models.CharField(u'相似部件', max_length=64, default='', blank=True)
    dup_id_final = models.CharField(u'重复ID', max_length=32, default='', blank=True)

    is_draft_equals_review = models.BooleanField(u'初次回查是否相等', choices=YESNO_CHOICES, default=False)
    is_review_equals_final = models.BooleanField(u'回查审查是否相等', choices=YESNO_CHOICES, default=False)
    is_checked = models.BooleanField(u'是否人工审核', choices=YESNO_CHOICES, default=False)
    is_submitted = models.BooleanField(u'是否入hanzi库', choices=YESNO_CHOICES, default=False)
    remark = models.CharField(u'备注', max_length=64, default='', blank=True)
    c_t = models.DateTimeField(u'创建时间', null=True, blank=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, blank=True, auto_now=True)
    task = GenericRelation(Tasks, related_query_name="split_task")

    class Meta:
        db_table = 'lq_variants_split'
        verbose_name = u"拆分"
        verbose_name_plural = u"拆分"

    def __unicode__(self):
        return self.hanzi_char + ':' + self.hanzi_pic_id


class InputPage(models.Model):
    page_num = models.SmallIntegerField(primary_key=True)
    task = GenericRelation(Tasks, related_query_name="page_task")

    class Meta:
        db_table = 'lq_input_page'

    def __unicode__(self):
        return str(self.page_num)


class VariantsInput(models.Model):
    volume_num = models.SmallIntegerField(u'册', default=0, blank=True)
    page_num = models.IntegerField(u'页码', default=0)
    # page_num = models.ForeignKey(InputPage, related_name='inputs', on_delete=models.SET_NULL, blank=True, null=True)

    seq_num_draft = models.SmallIntegerField(u'序号', default=0)
    hanzi_char_draft = models.CharField(u'文字', max_length=8, blank=True, default='')
    hanzi_pic_id_draft = models.CharField(u'图片字编码', max_length=32, blank=True, default='')
    variant_type_draft = models.SmallIntegerField(u'正异类型', choices=INPUT_VARIANT_TYPE_CHOICES, default=0)
    std_hanzi_draft = models.CharField(u'所属正字', max_length=64, blank=True, default='')
    notes_draft = models.CharField(u'注释信息', max_length=64, blank=True, default='')
    is_del_draft = models.BooleanField(u'是否删除', choices=YESNO_CHOICES, default=False)

    seq_num_review = models.SmallIntegerField(u'序号', default=0)
    hanzi_char_review = models.CharField(u'文字', max_length=8, blank=True, default='')
    hanzi_pic_id_review = models.CharField(u'图片字编码', max_length=32, blank=True, default='')
    variant_type_review = models.SmallIntegerField(u'正异类型', choices=INPUT_VARIANT_TYPE_CHOICES, default=0)
    std_hanzi_review = models.CharField(u'所属正字', max_length=64, blank=True, default='')
    notes_review = models.CharField(u'注释信息', max_length=64, blank=True, default='')
    is_del_review = models.BooleanField(u'是否删除', choices=YESNO_CHOICES, default=False)

    seq_num_final = models.SmallIntegerField(u'序号', default=0)
    hanzi_char_final = models.CharField(u'文字', max_length=8, blank=True, default='')
    hanzi_pic_id_final = models.CharField(u'图片字编码', max_length=32, blank=True, default='')
    variant_type_final = models.SmallIntegerField(u'正异类型', choices=INPUT_VARIANT_TYPE_CHOICES, default=0)
    std_hanzi_final = models.CharField(u'所属正字', max_length=64, blank=True, default='')
    notes_final = models.CharField(u'注释信息', max_length=64, blank=True, default='')
    is_del_final = models.BooleanField(u'是否删除', choices=YESNO_CHOICES, default=False)

    is_draft_equals_review = models.BooleanField(u'初次回查是否相等', choices=YESNO_CHOICES, default=False)
    is_review_equals_final = models.BooleanField(u'回查审查是否相等', choices=YESNO_CHOICES, default=False)
    is_checked = models.BooleanField(u'是否人工审核', choices=YESNO_CHOICES, default=False)
    is_submitted = models.BooleanField(u'是否入hanzi库', choices=YESNO_CHOICES, default=False)

    remark = models.CharField(u'备注', max_length=64, blank=True, default='')
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)
    task = GenericRelation(Tasks, related_query_name="input_task")

    class Meta:
        db_table = 'lq_variants_input'
        verbose_name = u"录入"
        verbose_name_plural = u"录入"

    def __unicode__(self):
        return '#' + str(self.page_num) + ':' + self.hanzi_char_draft + ':' + self.hanzi_pic_id_draft


class KoreanVariantsDict(models.Model):
    glyph = models.CharField(u'字形', max_length=16, blank=True, default='')
    code = models.CharField(u'Unicode', max_length=16, blank=True, default='')
    busu_id = models.IntegerField(u'部首ID，对应于hanzi_radicals的id', blank=True, default='')
    totalstrokes = models.SmallIntegerField(u'总笔画', blank=True, default='')
    reststrokes = models.SmallIntegerField(u'剩余笔画', blank=True, default='')
    jungma = models.CharField(u'郑码', max_length=64, blank=True, default='')
    standard = models.CharField(u'正字Unicode码', max_length=16, blank=True, default='')
    ksound = models.CharField(u'韩文发音', max_length=16, blank=True, default='')
    kmean = models.CharField(u'韩文含义', max_length=128, blank=True, default='')
    banjul = models.CharField(u'反切', max_length=64, blank=True, default='')
    csound = models.CharField(u'中文发音', max_length=64, blank=True, default='')
    cmean = models.CharField(u'中文含义', max_length=128, blank=True, default='')
    jsound = models.CharField(u'日文发音', max_length=64, blank=True, default='')
    jmean = models.CharField(u'日文含义', max_length=128, blank=True, default='')
    emean = models.CharField(u'英文含义', max_length=128, blank=True, default='')

    class Meta:
        db_table = 'lq_korean_variants_dict'
        verbose_name = u"高丽异体字典"
        verbose_name_plural = u"高丽异体字典"

    def __unicode__(self):
        return self.glyph + ':' + self.code


class HanziRadicals(models.Model):
    radical = models.CharField(u'部首', max_length=16, blank=True, default='')
    strokes = models.PositiveSmallIntegerField(u'笔画数', default=1)
    is_un_radical = models.SmallIntegerField(u'是否为Unicode部首', default=0)
    is_tw_radical = models.SmallIntegerField(u'是否为台湾异体字部首', default=0)
    is_zh_radical = models.SmallIntegerField(u'是否为汉语大字典部首', default=0)
    is_kr_radical = models.SmallIntegerField(u'是否为高丽异体字部首', default=0)
    is_dh_radical = models.SmallIntegerField(u'是否为敦煌俗字典部首', default=0)
    remark = models.CharField(u'备注', max_length=128, blank=True, default='')

    def __unicode__(self):
        return self.radical + ':' + self.strokes

    class Meta:
        db_table = 'lq_hanzi_radicals'
        ordering = ['strokes', 'id']
        verbose_name = u"汉字部首"
        verbose_name_plural = u"汉字部首"


class KoreanDupZhengCodes(models.Model):
    zheng_code = models.CharField(u'郑码', max_length=32, blank=True, default='')
    count = models.SmallIntegerField(u'郑码对应汉字的数量', blank=True)
    page_num = models.SmallIntegerField(u'页码', default=0)

    class Meta:
        db_table = 'lq_korean_dup_zheng_codes'
        verbose_name = u"高丽郑码"
        verbose_name_plural = u"高丽郑码"

    def __unicode__(self):
        return self.zheng_code + ':' + self.page_num


class KoreanDedup(models.Model):
    source = models.SmallIntegerField(u'来源', choices=SOURCE_CHOICES, default=0)
    hanzi_type = models.SmallIntegerField(u'字形类型：文字、图片、文字且图片', choices=HANZI_TYPE_CHOICES, default=0)
    hanzi_char = models.CharField(u'文字', max_length=8, blank=True, default='')
    hanzi_pic_id = models.CharField(u'图片字编码', max_length=32, blank=True, default='')
    variant_type = models.SmallIntegerField(u'正异类型', choices=VARIANT_TYPE_CHOICES, null=True)
    std_hanzi = models.CharField(u'所属正字', max_length=64, blank=True, default='')
    zheng_code = models.CharField(u'郑码', max_length=32, blank=True, default='')
    korean_dup_hanzi = models.CharField(u'异体字字典内部重复编码', max_length=32, blank=True, default='')
    remark = models.CharField(u'备注', max_length=64, blank=True, default='')
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)

    class Meta:
        db_table = 'lq_korean_dedup'
        verbose_name = u"高丽去重结果"
        verbose_name_plural = u"高丽去重结果"

    def __unicode__(self):
        return self.hanzi_char + ':' + self.hanzi_pic_id + ':' + self.korean_dup_hanzi


class KoreanDupCharacters(models.Model):
    korean_variant = models.CharField(u'高丽字头', max_length=32, blank=True)
    unicode = models.CharField(u'与字头字形相同/相近的Unicode', max_length=32, blank=True)
    relation = models.SmallIntegerField(u'二者关系：形码均相同，形似码相同，形同码不同，无相同字形', null=True)
    remark = models.CharField(u'备注', max_length=128, blank=True)
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)
    task = GenericRelation(Tasks, related_query_name="inter_dedup_task")

    class Meta:
        db_table = 'lq_korean_dup_characters'
        verbose_name = u"高台去重字头"
        verbose_name_plural = u"高台去重字头"

    def __unicode__(self):
        return self.korean_variant + " vs." + self.unicode


class InterDictDedup(models.Model):
    source = models.SmallIntegerField(u'来源', choices=SOURCE_CHOICES, default=0)
    hanzi_type = models.SmallIntegerField(u'字形类型：文字、图片、文字且图片', choices=HANZI_TYPE_CHOICES, default=0)
    hanzi_char = models.CharField(u'文字', max_length=8, blank=True)
    hanzi_pic_id = models.CharField(u'图片字编码', max_length=32, blank=True)
    variant_type = models.SmallIntegerField(u'正异类型', choices=VARIANT_TYPE_CHOICES, null=True)
    std_hanzi = models.CharField(u'所属正字', max_length=64, blank=True)
    as_std_hanzi = models.CharField(u'兼正字号', max_length=32, blank=True)
    inter_dict_dup_hanzi_draft = models.CharField(u'异体字字典间重复编码', max_length=64, blank=True)
    inter_dict_dup_hanzi_review = models.CharField(u'异体字字典间重复编码', max_length=64, blank=True)
    inter_dict_dup_hanzi_final = models.CharField(u'异体字字典间重复编码', max_length=64, blank=True)
    is_draft_equals_review = models.BooleanField(u'初次回查是否相等', choices=YESNO_CHOICES, default=False)
    is_review_equals_final = models.BooleanField(u'回查审查是否相等', choices=YESNO_CHOICES, default=False)
    is_checked = models.BooleanField(u'是否人工审核', choices=YESNO_CHOICES, default=False)
    is_submitted = models.BooleanField(u'是否入hanzi库', choices=YESNO_CHOICES, default=False)
    remark = models.CharField(u'备注', max_length=64, blank=True)
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)
    task = GenericRelation(Tasks, related_query_name="dedup_task")

    class Meta:
        db_table = 'lq_inter_dict_dedup'
        verbose_name = u"高台去重结果"
        verbose_name_plural = u"高台去重结果"

    def __unicode__(self):
        return self.hanzi_char + ':' + self.hanzi_pic_id + ':' + self.inter_dict_dup_hanzi_draft


class Reward(models.Model):
    reward_name = models.CharField(u'奖品名称', max_length=64)
    reward_quantity = models.SmallIntegerField(u'奖品数量', default=1)
    reward_pic = models.CharField(u'奖品图片', max_length=128)
    need_credits = models.SmallIntegerField(u'所需积分')

    class Meta:
        verbose_name = u"奖品"
        verbose_name_plural = u"奖品"
        db_table = 'lq_reward'

    def __unicode__(self):
        return self.reward_name + ':' + self.reward_quantity


class CreditsRedeem(models.Model):
    redeem_status_choices = ((0, u'申请中'), (1, u'已受理'), (2, u'已完成'))

    accepted_at = models.DateTimeField(u'受理时间', null=True, blank=True, default=timezone.now)
    completed_at = models.DateTimeField(u'完成时间', null=True, blank=True)
    reward_name = models.CharField(u'奖品名称', max_length=64)
    # reward = models.ForeignKey(Reward, related_name="reward", verbose_name="奖品")
    cost_credits = models.IntegerField(u'所用积分', null=True)

    status = models.SmallIntegerField(u'状态：申请中，已受理，已完成', choices=redeem_status_choices, default=0)
    remark = models.CharField(u'备注', max_length=64, null=True, blank=True)
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)
    accepted_by = models.ForeignKey(User, verbose_name=u"受理人", related_name="acceptor", null=True, blank=True)
    applied_by = models.ForeignKey(User, verbose_name=u"申请人", related_name="applier", null=True, blank=True)
    completed_by = models.ForeignKey(User, verbose_name=u"完成人", related_name="completor", null=True, blank=True)

    class Meta:
        db_table = 'lq_credits_redeem'
        verbose_name = verbose_name_plural = u"积分兑换"

    def __unicode__(self):
        return self.redeem_status_choices[self.status] + ':' + self.reward_name


class Diaries(models.Model):

    """
    打卡记录
    """
    tag_choices = ((0, u'问题反馈'), (1, u'心情故事'), (2, u'其他'))

    # user_id = models.IntegerField(u'用户id', null=True)
    tag = models.SmallIntegerField(u'标签', choices=tag_choices, default=0)
    work_types = models.CharField(u'工作类型', max_length=64, blank=True)
    work_brief = models.CharField(u'工作摘要，如：【拆字x个，去重y页，录入z个。】', max_length=512, blank=True)
    content = models.TextField(u'打卡日记', blank=True)
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)

    user = models.ForeignKey(User)

    class Meta:
        verbose_name = u"打卡记录"
        verbose_name_plural = u"打卡记录"
        db_table = 'lq_diaries'

    def __unicode__(self):
        return self.tag_choices[self.tag][1] + ':' + self.work_brief


class Credits(models.Model):

    """
    积分
    """
    sort_choices = ((0, u"总积分"), (1, u"拆字积分"), (5, u"去重积分"), (2, u"录入积分"), (3, u"图书校对"), (4, u"论文下载"))

    # user_id = models.IntegerField(u'用户id', null=True)
    credit = models.IntegerField(u"积分值", default=0)
    user = models.ForeignKey(User, verbose_name=u"用户", related_name="user_credits")
    sort = models.IntegerField(u"积分类型", choices=sort_choices, default=1)
    u_t = models.DateTimeField(u'更新时间', auto_now=True)

    class Meta:
        verbose_name = u"积分"
        verbose_name_plural = u"积分"
        db_table = 'lq_credits'
        ordering = ["-credit"]

    def __unicode__(self):
        return str(self.sort)+str(self.credit)


# Operation log table
class Operation(models.Model):
    log_type_choices = (
        (0, u'常规日志'),
        (1, u'任务包管理'),
        (2, u'任务管理'),
        (3, u'奖品管理'),
        (4, u'讨论区管理'),
        (5, u'用户管理'),
    )
    user = models.ForeignKey(User, models.SET_NULL, null=True)
    logtype = models.IntegerField(u'日志类型', choices=log_type_choices, default=0)
    message = models.CharField(u'日志内容', max_length=1024)
    logtime = models.DateTimeField(u'记录时间', auto_now=True)

    def __unicode__(self):
        return self.message

    class Meta:
        db_table = 'operation_log'


class HanziParts(models.Model):
    cancan_choices = ((0, u'不可'), (1, u'可'))
    hspnz_hash = {'1': 'h', '2': 's', '3': 'p', '4': 'n', '5': 'z'}

    part_char = models.CharField(u'部首文字', blank=True, max_length=8)
    is_split_part = models.SmallIntegerField(u'可拆分', choices=cancan_choices, default=0)
    is_search_part = models.SmallIntegerField(u'可搜索', choices=cancan_choices, default=0)
    replace_parts = models.CharField(u'替换部件', max_length=64, blank=True)
    strokes = models.SmallIntegerField(u'笔画数', default=1)
    stroke_order = models.CharField(u'笔顺', max_length=64, blank=True)
    remark = models.CharField(u'备注', max_length=64, blank=True)

    def __unicode__(self):
        return self.part_char

    class Meta:
        db_table = 'lq_hanzi_parts'
        verbose_name = u"汉字部件"
        verbose_name_plural = u"汉字部件"

    @property
    def stroke_hspnz(self):
        return ''.join(map(lambda x: HanziParts.hspnz_hash[x], self.stroke_order))

    @property
    def display(self):
        return self.part_char

    @property
    def input(self):
        return self.part_char


class UserTaskProfile(models.Model):
    user = models.ForeignKey(User)
    last_split_id = models.IntegerField(u'上次拆分工作的ID', default=0)
    last_dedup_id = models.IntegerField(u'上次去重工作的ID', default=0)
    last_input_id = models.IntegerField(u'上次录入工作的ID', default=0)
    u_t = models.DateTimeField(u'更新时间', auto_now=True)

    class Meta:
        db_table = 'lq_user_task_profile'
        verbose_name = u'用户任务状态'
        verbose_name_plural = u'用户任务状态'
