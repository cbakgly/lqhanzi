# -*- coding:utf8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
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

    def __unicode__(self):
        return self.username


variant_type_choices = ((0, '纯正字'), (1, '狭义异体字'), (2, '广义且正字'), (3, '广义异体字'), (4, '狭义且正字'), (5, '特定异体字'), (6, '特定且正字'), (7, '误刻误印'), (8, '其他不入库类型'), (9, '其他入库类型'))
hanzi_type_choices = ((0, '文字'), (1, '图片'), (2, '文字且图片'))


class HanziSet(models.Model):
    source = models.SmallIntegerField(u'来源', null=True)
    hanzi_type = models.SmallIntegerField(u'字形类型：文字、图片、文字且图片', choices=hanzi_type_choices, null=True, blank=True)
    hanzi_char = models.CharField(u'文字', null=True, max_length=8)
    hanzi_pic_id = models.CharField(u'图片字编码', null=True, max_length=32)

    variant_type = models.SmallIntegerField(u'正异类型', choices=variant_type_choices, null=True, blank=True)
    std_hanzi = models.CharField(u'所属正字', null=True, max_length=64)
    as_std_hanzi = models.CharField(u'兼正字号', null=True, max_length=32)
    seq_id = models.CharField(u'字的位置统一编码', null=True, max_length=32)

    pinyin = models.CharField(u'拼音', null=True, max_length=64)
    radical = models.CharField(u'部首', null=True, max_length=8)
    strokes = models.SmallIntegerField(u'笔画数', null=True)
    zheng_code = models.CharField(u'郑码', null=True, max_length=32)
    wubi = models.CharField(u'五笔', null=True, max_length=32)

    dup_count = models.SmallIntegerField(u'重复次数', null=True)
    inter_dict_dup_hanzi = models.CharField(u'异体字字典间重复编码', null=True, max_length=64)
    korean_dup_hanzi = models.CharField(u'高丽异体字字典内部重复编码', null=True, max_length=32)
    is_korean_redundant = models.SmallIntegerField(u'是否多余高丽异体字', null=True)
    is_inter_dict_redundant = models.SmallIntegerField(u'是否多余台湾高丽异体字', null=True)

    skip_num = models.SmallIntegerField(u'跳过次数，多的话算难字', null=True)
    structure = models.CharField(u'结构', max_length=16, null=True)
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
        db_table = 'lq_hanzi_set'


class VariantsSplit(models.Model):
    source = models.SmallIntegerField(u'来源', null=True, blank=True)
    hanzi_type = models.SmallIntegerField(u'字形类型：文字、图片、文字且图片', choices=hanzi_type_choices, null=True, blank=True)
    hanzi_char = models.CharField(u'文字', null=True, blank=True, max_length=8)
    hanzi_pic_id = models.CharField(u'图片字编码', null=True, blank=True, max_length=32)

    variant_type = models.SmallIntegerField(u'正异类型', choices=variant_type_choices, null=True, blank=True)
    std_hanzi = models.CharField(u'所属正字', null=True, blank=True, max_length=64)
    as_std_hanzi = models.CharField(u'兼正字号', null=True, blank=True, max_length=32)
    seq_id = models.CharField(u'字的位置统一编码', null=True, blank=True, max_length=32)
    is_redundant = models.SmallIntegerField(u'是否多余', null=True, blank=True)

    skip_num_draft = models.SmallIntegerField(u'太难跳过次数', null=True, blank=True)
    init_split_draft = models.CharField(u'初步拆分', max_length=128, null=True, blank=True)
    other_init_split_draft = models.CharField(u'其它初步拆分', max_length=128, null=True, blank=True)
    deform_split_draft = models.CharField(u'调笔拆分', max_length=128, null=True, blank=True)
    similar_parts_draft = models.CharField(u'相似部件', max_length=64, null=True, blank=True)
    dup_id_draft = models.CharField(u'重复ID', max_length=32, null=True, blank=True)

    skip_num_review = models.SmallIntegerField(u'太难跳过次数', null=True, blank=True)
    init_split_review = models.CharField(u'初步拆分', max_length=128, null=True, blank=True)
    other_init_split_review = models.CharField(u'其它初步拆分', max_length=128, null=True, blank=True)
    deform_split_review = models.CharField(u'调笔拆分', max_length=128, null=True, blank=True)
    similar_parts_review = models.CharField(u'相似部件', max_length=64, null=True, blank=True)
    dup_id_review = models.CharField(u'重复ID', max_length=32, null=True, blank=True)

    skip_num_final = models.SmallIntegerField(u'太难跳过次数', null=True, blank=True)
    init_split_final = models.CharField(u'初步拆分', max_length=128, null=True, blank=True)
    other_init_split_final = models.CharField(u'其它初步拆分', max_length=128, null=True, blank=True)
    deform_split_final = models.CharField(u'调笔拆分', max_length=128, null=True, blank=True)
    similar_parts_final = models.CharField(u'相似部件', max_length=64, null=True, blank=True)
    dup_id_final = models.CharField(u'重复ID', max_length=32, null=True, blank=True)

    is_draft_equals_review = models.SmallIntegerField(u'初次回查是否相等', null=True, blank=True)
    is_review_equals_final = models.SmallIntegerField(u'回查审查是否相等', null=True, blank=True)
    is_checked = models.SmallIntegerField(u'是否人工审核', default=0)
    is_submitted = models.SmallIntegerField(u'是否入hanzi库', default=0)
    remark = models.CharField(u'备注', max_length=64, null=True, blank=True)
    c_t = models.DateTimeField(u'创建时间', null=True, blank=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, blank=True, auto_now=True)

    class Meta:
        db_table = 'lq_variants_split'

    def __unicode__(self):
        return self.hanzi_char


class VariantsInput(models.Model):
    volume_num = models.SmallIntegerField(u'册', null=True, blank=True)
    page_num = models.IntegerField(u'页码', null=True)

    seq_num_draft = models.SmallIntegerField(u'序号', null=True)
    hanzi_char_draft = models.CharField(u'文字', max_length=8, null=True)
    hanzi_pic_id_draft = models.CharField(u'图片字编码', max_length=32, null=True)
    variant_type_draft = models.SmallIntegerField(u'正异类型', choices=variant_type_choices, null=True)
    std_hanzi_draft = models.CharField(u'所属正字', max_length=64, null=True)
    notes_draft = models.CharField(u'注释信息', max_length=64, null=True)
    is_del_draft = models.SmallIntegerField(u'是否删除', null=True)

    seq_num_review = models.SmallIntegerField(u'序号', null=True)
    hanzi_char_review = models.CharField(u'文字', max_length=8, null=True)
    hanzi_pic_id_review = models.CharField(u'图片字编码', max_length=32, null=True)
    variant_type_review = models.SmallIntegerField(u'正异类型', choices=variant_type_choices, null=True)
    std_hanzi_review = models.CharField(u'所属正字', max_length=64, null=True)
    notes_review = models.CharField(u'注释信息', max_length=64, null=True)
    is_del_review = models.SmallIntegerField(u'是否删除', null=True)

    seq_num_final = models.SmallIntegerField(u'序号', null=True)
    hanzi_char_final = models.CharField(u'文字', max_length=8, null=True)
    hanzi_pic_id_final = models.CharField(u'图片字编码', max_length=32, null=True)
    variant_type_final = models.SmallIntegerField(u'正异类型', choices=variant_type_choices, null=True)
    std_hanzi_final = models.CharField(u'所属正字', max_length=64, null=True)
    notes_final = models.CharField(u'注释信息', max_length=64, null=True)
    is_del_final = models.SmallIntegerField(u'是否删除', null=True)

    is_draft_equals_review = models.SmallIntegerField(u'初次回查是否相等', null=True)
    is_review_equals_final = models.SmallIntegerField(u'回查审查是否相等', null=True)
    is_checked = models.SmallIntegerField(u'是否人工审核', default=0)
    is_submitted = models.SmallIntegerField(u'是否入hanzi库', default=0)

    remark = models.CharField(u'备注', max_length=64, null=True)
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)

    class Meta:
        db_table = 'lq_variants_input'


class KoreanVariantsDict(models.Model):
    glyph = models.CharField(u'字形', max_length=16, null=True)
    code = models.CharField(u'Unicode', max_length=16, null=True)
    busu_id = models.IntegerField(u'部首ID，对应于hanzi_radicals的id', null=True)
    totalstrokes = models.SmallIntegerField(u'总笔画', null=True)
    reststrokes = models.SmallIntegerField(u'剩余笔画', null=True)
    jungma = models.CharField(u'郑码', max_length=64, null=True)
    standard = models.CharField(u'正字Unicode码', max_length=16, null=True)
    ksound = models.CharField(u'韩文发音', max_length=16, null=True)
    kmean = models.CharField(u'韩文含义', max_length=128, null=True)
    banjul = models.CharField(u'反切', max_length=64, null=True)
    csound = models.CharField(u'中文发音', max_length=64, null=True)
    cmean = models.CharField(u'中文含义', max_length=128, null=True)
    jsound = models.CharField(u'日文发音', max_length=64, null=True)
    jmean = models.CharField(u'日文含义', max_length=128, null=True)
    emean = models.CharField(u'英文含义', max_length=128, null=True)

    class Meta:
        db_table = 'lq_korean_variants_dict'


class HanziRadicals(models.Model):
    radical = models.CharField(u'部首', max_length=16, null=True)
    strokes = models.SmallIntegerField(u'笔画数', null=True)

    class Meta:
        db_table = 'lq_hanzi_radicals'


class KoreanDupZhengCodes(models.Model):
    zheng_code = models.CharField(u'郑码', max_length=32, null=True)
    count = models.SmallIntegerField(u'郑码对应汉字的数量', null=True)
    page_num = models.SmallIntegerField(u'页码', null=True)

    class Meta:
        db_table = 'lq_korean_dup_zheng_codes'


class KoreanDedup(models.Model):
    source = models.SmallIntegerField(u'来源', null=True)
    hanzi_type = models.SmallIntegerField(u'字形类型：文字、图片、文字且图片', choices=hanzi_type_choices, null=True)
    hanzi_char = models.CharField(u'文字', max_length=8, null=True)
    hanzi_pic_id = models.CharField(u'图片字编码', max_length=32, null=True)
    variant_type = models.SmallIntegerField(u'正异类型', choices=variant_type_choices, null=True)
    std_hanzi = models.CharField(u'所属正字', max_length=64, null=True)
    zheng_code = models.CharField(u'郑码', max_length=32, null=True)
    korean_dup_hanzi = models.CharField(u'异体字字典内部重复编码', max_length=32, null=True)
    remark = models.CharField(u'备注', max_length=64, null=True)
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)

    class Meta:
        db_table = 'lq_korean_dedup'


class KoreanDupCharacters(models.Model):
    korean_variant = models.CharField(u'高丽字头', max_length=32, null=True)
    unicode_of_korean = models.CharField(u'与字头字形相同/相近的Unicode', max_length=32, null=True)
    relation = models.SmallIntegerField(u'二者关系：形码均相同，形似码相同，形同码不同，无相同字形', null=True)
    remark = models.CharField(u'备注', max_length=128, null=True)
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)

    class Meta:
        db_table = 'lq_korean_dup_characters'


class InterDictDedup(models.Model):
    source = models.SmallIntegerField(u'来源', null=True)
    hanzi_type = models.SmallIntegerField(u'字形类型：文字、图片、文字且图片', choices=hanzi_type_choices, null=True)
    hanzi_char = models.CharField(u'文字', max_length=8, null=True)
    hanzi_pic_id = models.CharField(u'图片字编码', max_length=32, null=True)
    variant_type = models.SmallIntegerField(u'正异类型', choices=variant_type_choices, null=True)
    std_hanzi = models.CharField(u'所属正字', max_length=64, null=True)
    as_std_hanzi = models.CharField(u'兼正字号', max_length=32, null=True)
    inter_dict_dup_hanzi_draft = models.CharField(u'异体字字典间重复编码', max_length=64, null=True)
    inter_dict_dup_hanzi_review = models.CharField(u'异体字字典间重复编码', max_length=64, null=True)
    inter_dict_dup_hanzi_final = models.CharField(u'异体字字典间重复编码', max_length=64, null=True)
    is_draft_equals_review = models.SmallIntegerField(u'初次回查是否相等', null=True)
    is_review_equals_final = models.SmallIntegerField(u'回查审查是否相等', null=True)
    is_checked = models.SmallIntegerField(u'是否人工审核', default=0)
    is_submitted = models.SmallIntegerField(u'是否入hanzi库', default=0)
    remark = models.CharField(u'备注', max_length=64, null=True)
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)

    class Meta:
        db_table = 'lq_inter_dict_dedup'


business_type_choices = ((0, u'录入'), (1, u'拆字'), (2, u'去重'), (3, u'互助'))
business_stage_choices = ((0, u'初次'), (1, u'回查'), (2, u'审查'))
status_choices = ((0, u'进行中'), (1, u'已完成'))


class TaskPackages(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name="user_tps")  # 用户，拆字员
    business_type = models.SmallIntegerField(u'任务类型', choices=business_type_choices, null=True)
    business_stage = models.SmallIntegerField(u'任务阶段', choices=business_stage_choices, null=True)
    size = models.SmallIntegerField(u'工作包大小', null=False, default=100)
    status = models.SmallIntegerField(u'工作包状态', choices=status_choices, default=0)
    daily_plan = models.SmallIntegerField(u'日计划工作量', null=False, default=5)
    due_date = models.DateTimeField(u'预计完成时间', null=True)
    completed_num = models.SmallIntegerField(u'已完成数量', default=0)
    completed_at = models.DateTimeField(u'完成时间', null=True)
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)

    class Meta:
        db_table = 'lq_task_packages'

    def __unicode__(self):
        return str(self.id)


class TaskTypes(models.Model):
    business_type = models.SmallIntegerField(u'任务类型', choices=business_type_choices, null=True)
    business_name = models.CharField(u'任务名称', max_length=64, null=True)
    credits = models.SmallIntegerField(u'单个任务积分', default=0)
    is_active = models.SmallIntegerField(u'是否启用', default=1)

    class Meta:
        db_table = 'lq_task_types'


class Tasks(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name="user_task")  # 用户，拆字员
    variant_split = models.ForeignKey(VariantsSplit, models.SET_NULL, related_name="split_task", null=True, blank=True)
    variant_input = models.ForeignKey(VariantsInput, models.SET_NULL, related_name="input_task", null=True, blank=True)
    korean_dedup = models.ForeignKey(KoreanDedup, models.SET_NULL, related_name="korean_dedup_task", null=True, blank=True)
    interdict_dedup = models.ForeignKey(InterDictDedup, models.SET_NULL, related_name="inter_dedup_task", null=True, blank=True)
    task_package = models.ForeignKey(TaskPackages, related_name='tasks', on_delete=models.CASCADE, blank=True, null=True)

    business_type = models.SmallIntegerField(u'任务类型', choices=business_type_choices, null=True)
    business_stage = models.SmallIntegerField(u'任务阶段', choices=business_stage_choices, null=True)
    task_status = models.SmallIntegerField(u'任务状态', choices=status_choices, null=True)

    credits = models.SmallIntegerField(u'积分', null=True)
    remark = models.CharField(u'备注', max_length=128, null=True, blank=True)

    assigned_at = models.DateTimeField(u'分配时间', null=True, default=timezone.now)
    completed_at = models.DateTimeField(u'完成时间', null=True)
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)

    class Meta:
        db_table = 'lq_tasks'

    def __unicode__(self):
        return "#" + self.business_type_choices[self.business_type][1] + self.business_stage_choices[self.business_stage][1] + str(self.id)


class CreditsRedeem(models.Model):
    redeem_status_choices = ((0, '申请中'), (1, '已受理'), (2, '已完成'))

    applied_by = models.ForeignKey(User, verbose_name="申请人", related_name="applier")
    accepted_by = models.ForeignKey(User, verbose_name="受理人", related_name="acceptor")
    completed_by = models.ForeignKey(User, verbose_name="完成人", related_name="completor")
    accepted_at = models.DateTimeField(u'受理时间', null=True)
    completed_at = models.DateTimeField(u'完成时间', null=True)
    reward_name = models.CharField(u'奖品名称', max_length=64, null=True)
    cost_credits = models.IntegerField(u'所用积分', null=True)

    status = models.SmallIntegerField(u'状态：申请中，已受理，已完成', choices=redeem_status_choices, null=True)
    remark = models.CharField(u'备注', max_length=64, null=True)
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)

    class Meta:
        db_table = 'lq_credits_redeem'


class Diaries(models.Model):
    """
    打卡记录
    """
    tag_choices = ((0, '问题反馈'), (1, '心情故事'), (2, '其他'))

    # user_id = models.IntegerField(u'用户id', null=True)
    user = models.ForeignKey(User)
    tag = models.SmallIntegerField(u'标签', choices=tag_choices, default=0)
    work_types = models.CharField(u'工作类型', max_length=64, null=True)
    work_brief = models.CharField(u'工作摘要，如：【拆字x个，去重y页，录入z个。】', max_length=512, null=True)
    content = models.TextField(u'打卡日记', null=True)
    c_t = models.DateTimeField(u'创建时间', null=True, default=timezone.now)
    u_t = models.DateTimeField(u'修改时间', null=True, auto_now=True)

    class Meta:
        verbose_name = "打卡记录"
        verbose_name_plural = "打卡记录"
        db_table = 'lq_diaries'

    def __unicode__(self):
        return self.work_brief


class Credits(models.Model):
    """
    积分
    """
    sort_choices = ((1, u"总积分"), (2, u"拆字积分"), (3, u"去重积分"), (4, u"录入积分"), (5, u"互助积分"))

    # user_id = models.IntegerField(u'用户id', null=True)
    user = models.ForeignKey(User, verbose_name="用户", related_name="user_credits")
    credit = models.IntegerField(u"积分值", null=True)
    sort = models.IntegerField(u"积分类型", choices=sort_choices, default=1)

    class Meta:
        verbose_name = "积分"
        verbose_name_plural = "积分"
        db_table = 'lq_credits'
        ordering = ["-credit"]

    def __unicode__(self):
        return self.sort.credit_sort


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
