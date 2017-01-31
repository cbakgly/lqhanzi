# -*- coding:utf8 -*-

# 集中将业务上的枚举类型的工具函数写在这里


TASK_PACKAGE_STATUS_ENUM = {"ongoing": 0, "completed": 1}
TASK_STATUS_ENUM = {"closed": 0, "to_be_arranged": 1, "ongoing": 2, "completed": 3}
BUSINESS_TYPE_ENUM = {"split": 1, "input": 2, "book": 3, "download": 4, "dedup": 5, "help": 7, "input_page": 9, "dedup_child": 8}
BUSINESS_STAGE_ENUM = {'init': 1, 'review': 2, 'final': 3}
SOURCE_ENUM = {'unicode': 1, 'taiwan': 2, 'hanyu': 3, 'korean': 4, 'dunhuang': 5}


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
