# -*- coding:utf8 -*-

# 集中将业务上的枚举类型的工具函数写在这里


TASK_PACKAGE_STATUS_ENUM = {"ongoing": 0, "completed": 1}
TASK_STATUS_ENUM = {"closed": 0, "to_be_arranged": 1, "ongoing": 2, "completed": 3}
BUSINESS_TYPE_ENUM = {"split": 1, "input": 2, "book": 3, "download": 4, "dedup": 5, "help": 7, "input_page": 9, "dedup_child": 8}
BUSINESS_STAGE_ENUM = {'init': 1, 'review': 2, 'final': 3}
SOURCE_ENUM = {'unicode': 1, 'taiwan': 2, 'hanyu': 3, 'korean': 4, 'dunhuang': 5}
GROUPS = {"guest": 1, "member": 2, "volunteer ": 3, "forum_manager ": 4, "op_manager ": 5, "draft_split ": 6,
          "review_split ": 7, "final_split ": 8, "draft_dedup ": 9, "review_dedup ": 10,
          "final_dedup ": 11, "draft_input ": 12, "review_input ": 13, "final_input ": 14}
PERMS = {'draft_input': 'backend.op_draft_input', 'review_input': 'backend.op_review_input', 'final_input': 'backend.op_final_input',
         'draft_split': 'backend.op_draft_split', 'review_split': 'backend.op_review_split', 'final_split': 'backend.op_final_split',
         'draft_dedup': 'backend.op_draft_dedup', 'review_dedup': 'backend.op_review_dedup', 'final_dedup': 'backend.op_final_dedup'}
CREDIT_TYPE = {0: '总积分', 1: '拆字积分', 2: '录入积分', 3: '图书校对', 4: '论文下载', 5: '去重积分'}
VARIANT_TYPE = {'STDANDARD': 0, 'VARIANT_NARROW': 1, 'STDANDARD_VARIANT_WIDE': 2, 'VARIANT_WIDE': 3}
VARIANT_TYPE_INVERSE = {0: '正字', 1: '狭义异体字', 2: '广义且正字', 3: '广义异体字'}


def getenum_task_package_status(name):
    return TASK_PACKAGE_STATUS_ENUM[name]


def getenum_task_status(name):
    return TASK_STATUS_ENUM[name]


def getenum_business_type(name):
    return BUSINESS_TYPE_ENUM[name]


def getenum_source(name):
    return SOURCE_ENUM[name]


def getenum_business_stage(name):
    return BUSINESS_STAGE_ENUM[name]


def getenum_group_id(name):
    return GROUPS[name]


def getenum_perm_code(name):
    return PERMS[name]


def getenum_credit_type(no):
    return CREDIT_TYPE[no]
