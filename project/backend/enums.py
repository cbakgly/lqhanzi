# -*- coding:utf8 -*-

# 集中将业务上的枚举类型的工具函数写在这里


def getenum_task_package_business_status(name):
    status = {"ongoing": 0, "completed": 1}
    return status[name]


def getenum_task_business_status(name):
    status = {"closed": 0, "to_be_arranged": 1, "ongoing": 2, "completed": 3}
    return status[name]


def getenum_business_type(name):
    type = {"input": 2, "split": 1, "dedup": 5, "help": 7}
    return type[name]


def getenum_source(name):
    lists = {'unicode': 1, 'taiwan': 2, 'hanyu': 3, 'korean': 4, 'dunhuang': 5}
    return lists[name]


def getenum_business_stage(name):
    stage = {'init': 1, 'review': 2, 'final': 3}
    return stage[name]
