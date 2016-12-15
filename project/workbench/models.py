# encoding: utf-8

from __future__ import unicode_literals

from django.db import models


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
    c_t = models.IntegerField(u'创建时间')
    u_t = models.IntegerField(u'修改时间')


class VariantsSplit(models.Model):
    source = models.SmallIntegerField(u'来源', null=True)
    hanzi_type = models.SmallIntegerField(u'字形类型：文字、图片、文字且图片', null=True)
    hanzi_char = models.CharField(u'文字', null=True, max_length=8)
    hanzi_pic_id = models.CharField(u'图片字编码', null=True, max_length=32)
    variant_type = models.SmallIntegerField(u'正异类型', null=True)
    std_hanzi = models.CharField(u'所属正字', null=True, max_length=64)
    as_std_hanzi = models.CharField(u'兼正字号', null=True, max_length=32)
    seq_id = models.CharField(u'字的位置统一编码', null=True, max_length=32)
    is_redundant = models.SmallIntegerField(u'是否多余', null=True)

    skip_num_draft = models.SmallIntegerField(u'太难跳过次数', null=True)
    init_split_draft = models.CharField(u'初步拆分', max_length=128, null=True)
    other_init_split_draft = models.CharField(u'其它初步拆分', max_length=128, null=True)
    deform_split_draft = models.CharField(u'调笔拆分', max_length=128, null=True)
    similar_parts_draft = models.CharField(u'相似部件', max_length=64, null=True)
    dup_id_draft = models.CharField(u'重复ID', max_length=32, null=True)

    skip_num_review = models.SmallIntegerField(u'太难跳过次数', null=True)
    init_split_review = models.CharField(u'初步拆分', max_length=128, null=True)
    other_init_split_review = models.CharField(u'其它初步拆分', max_length=128, null=True)
    deform_split_review = models.CharField(u'调笔拆分', max_length=128, null=True)
    similar_parts_review = models.CharField(u'相似部件', max_length=64, null=True)
    dup_id_review = models.CharField(u'重复ID', max_length=32, null=True)

    skip_num_final = models.SmallIntegerField(u'太难跳过次数', null=True)
    init_split_final = models.CharField(u'初步拆分', max_length=128, null=True)
    other_init_split_final = models.CharField(u'其它初步拆分', max_length=128, null=True)
    deform_split_final = models.CharField(u'调笔拆分', max_length=128, null=True)
    similar_parts_final = models.CharField(u'相似部件', max_length=64, null=True)
    dup_id_final = models.CharField(u'重复ID', max_length=32, null=True)

    is_draft_equals_review = models.SmallIntegerField(u'初次回查是否相等', null=True)
    is_review_equals_final = models.SmallIntegerField(u'回查审查是否相等', null=True)
    is_checked = models.SmallIntegerField(u'是否人工审核', default=0)
    is_submitted = models.SmallIntegerField(u'是否入hanzi库', default=0)
    remark = models.CharField(u'备注', max_length=64, null=True)
    c_t = models.IntegerField(u'创建时间')
    u_t = models.IntegerField(u'修改时间')


class VariantsInput(models.Model):
    volume_num = models.SmallIntegerField(u'册', null=True)
    page_num = models.IntegerField(u'页码', null=True)

    seq_num_draft = models.SmallIntegerField(u'序号', null=True)
    hanzi_char_draft = models.CharField(u'文字', max_length=8, null=True)
    hanzi_pic_id_draft = models.CharField(u'图片字编码', max_length=32, null=True)
    variant_type_draft = models.SmallIntegerField(u'正异类型', null=True)
    std_hanzi_draft = models.CharField(u'所属正字', max_length=64, null=True)
    notes_draft = models.CharField(u'注释信息', max_length=64, null=True)
    is_del_draft = models.SmallIntegerField(u'是否删除', null=True)

    seq_num_review = models.SmallIntegerField(u'序号', null=True)
    hanzi_char_review = models.CharField(u'文字', max_length=8, null=True)
    hanzi_pic_id_review = models.CharField(u'图片字编码', max_length=32, null=True)
    variant_type_review = models.SmallIntegerField(u'正异类型', null=True)
    std_hanzi_review = models.CharField(u'所属正字', max_length=64, null=True)
    notes_review = models.CharField(u'注释信息', max_length=64, null=True)
    is_del_review = models.SmallIntegerField(u'是否删除', null=True)

    seq_num_final = models.SmallIntegerField(u'序号', null=True)
    hanzi_char_final = models.CharField(u'文字', max_length=8, null=True)
    hanzi_pic_id_final = models.CharField(u'图片字编码', max_length=32, null=True)
    variant_type_final = models.SmallIntegerField(u'正异类型', null=True)
    std_hanzi_final = models.CharField(u'所属正字', max_length=64, null=True)
    notes_final = models.CharField(u'注释信息', max_length=64, null=True)
    is_del_final = models.SmallIntegerField(u'是否删除', null=True)

    is_draft_equals_review = models.SmallIntegerField(u'初次回查是否相等', null=True)
    is_review_equals_final = models.SmallIntegerField(u'回查审查是否相等', null=True)
    is_checked = models.SmallIntegerField(u'是否人工审核', default=0)
    is_submitted = models.SmallIntegerField(u'是否入hanzi库', default=0)

    remark = models.CharField(u'备注', max_length=64, null=True)
    c_t = models.IntegerField(u'创建时间')
    u_t = models.IntegerField(u'修改时间')


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


class HanziRadicals(models.Model):
    radical = models.CharField(u'部首', max_length=16, null=True)
    strokes = models.SmallIntegerField(u'笔画数', null=True)


class KoreanDupZhengCodes(models.Model):
    #zheng_code = emean = models.CharField(u'郑码', max_length=32, null=True)
    count = models.SmallIntegerField(u'郑码对应汉字的数量', null=True)
    page_num = models.SmallIntegerField(u'页码', null=True)


class KoreanDedup(models.Model):
    source = models.SmallIntegerField(u'来源', null=True)
    hanzi_type = models.SmallIntegerField(u'字形类型：文字、图片、文字且图片', null=True)
    hanzi_char = models.CharField(u'文字', max_length=8, null=True)
    hanzi_pic_id = models.CharField(u'图片字编码', max_length=32, null=True)
    variant_type = models.SmallIntegerField(u'正异类型', null=True)
    std_hanzi = models.CharField(u'所属正字', max_length=64, null=True)
    zheng_code = models.CharField(u'郑码', max_length=32, null=True)
    korean_dup_hanzi = models.CharField(u'异体字字典内部重复编码', max_length=32, null=True)
    remark = models.CharField(u'备注', max_length=64, null=True)
    c_t = models.IntegerField(u'创建时间')
    u_t = models.IntegerField(u'修改时间')


class KoreanDupCharacters(models.Model):
    korean_variant = models.CharField(u'高丽字头', max_length=32, null=True)
    unicode_of_korean = models.CharField(u'与字头字形相同/相近的Unicode', max_length=32, null=True)
    relation = models.SmallIntegerField(u'二者关系：形码均相同，形似码相同，形同码不同，无相同字形', null=True)
    remark = models.CharField(u'备注', max_length=128, null=True)
    c_t = models.IntegerField(u'创建时间', null=True)
    u_t = models.IntegerField(u'修改时间', null=True)


class InterDictDedup(models.Model):
    source = models.SmallIntegerField(u'来源', null=True)
    hanzi_type = models.SmallIntegerField(u'字形类型：文字、图片、文字且图片', null=True)
    hanzi_char = models.CharField(u'文字', max_length=8, null=True)
    hanzi_pic_id = models.CharField(u'图片字编码', max_length=32, null=True)
    variant_type = models.SmallIntegerField(u'正异类型', null=True)
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
    c_t = models.IntegerField(u'创建时间')
    u_t = models.IntegerField(u'修改时间')


class Tasks(models.Model):
    user_id = models.IntegerField(u'拆字员', null=True)
    business_id = models.IntegerField(u'业务ID，指的是对应于拆字、去重、录入业务表的ID', null=True)
    task_package_id = models.IntegerField(u'任务包ID', null=True)
    business_type = models.SmallIntegerField(u'任务类型', null=True)
    business_stage = models.SmallIntegerField(u'任务阶段', null=True)
    task_status = models.SmallIntegerField(u'任务状态', null=True)
    credits = models.SmallIntegerField(u'积分', null=True)
    remark = models.CharField(u'备注', max_length=128, null=True)
    assigned_at = models.IntegerField(u'分配时间', null=True)
    completed_at = models.IntegerField(u'完成时间', null=True)
    c_t = models.IntegerField(u'创建时间', null=True)
    u_t = models.IntegerField(u'修改时间', null=True)


class TaskPackages(models.Model):
    user_id = models.IntegerField(u'用户id', null=True)
    business_type = models.SmallIntegerField(u'任务类型', null=True)
    business_stage = models.SmallIntegerField(u'任务阶段', null=True)
    size = models.SmallIntegerField(u'工作包大小', null=True)
    status = models.SmallIntegerField(u'工作包状态', null=True)
    daily_plan = models.SmallIntegerField(u'日计划工作量', null=True)
    due_date = models.IntegerField(u'预计完成时间', null=True)
    completed_num = models.SmallIntegerField(u'已完成数量', null=True)
    completed_at = models.IntegerField(u'完成时间', null=True)
    c_t = models.IntegerField(u'创建时间', null=True)
    u_t = models.IntegerField(u'修改时间', null=True)


class CreditsRedeem(models.Model):
    applied_by = models.IntegerField(u'申请人的用户id', null=True)
    accepted_by = models.IntegerField(u'受理人的用户id', null=True)
    completed_by = models.IntegerField(u'完成人的用户id', null=True)
    accepted_at = models.IntegerField(u'受理时间', null=True)
    completed_at = models.IntegerField(u'完成时间', null=True)
    reward_name = models.CharField(u'奖品名称', max_length=64, null=True)
    cost_credits = models.IntegerField(u'所用积分', null=True)
    status = models.SmallIntegerField(u'状态：申请中，已受理，已完成', null=True)
    remark = models.CharField(u'备注', max_length=64, null=True)
    c_t = models.IntegerField(u'申请时间', null=True)
    u_t = models.IntegerField(u'修改时间', null=True)


class Diaries(models.Model):
    user_id = models.IntegerField(u'用户id', null=True)
    tag = models.SmallIntegerField(u'标签', null=True)
    work_types = models.CharField(u'工作类型', max_length=64, null=True)
    work_brief = models.CharField(u'工作摘要，如：【拆字x个，去重y页，录入z个。】', max_length=512, null=True)
    content = models.TextField(u'打卡日记', null=True)
    c_t = models.IntegerField(u'创建时间', null=True)
    u_t = models.IntegerField(u'修改时间', null=True)
