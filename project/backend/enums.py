# -*- coding:utf8 -*-

# 集中将业务上的枚举类型的工具函数写在这里


def getenum_business_status(name):
    status = {"closed": 0, "to_be_arranged": 1, "ongoing": 2, "completed": 3}
    return status[name]


def getenum_business_type(name):
    type = {"input": 1, "split": 0, "dedup": 2, "help": 3}
    return type[name]


def getenum_source(name):
    list = {'unicode': 1, 'taiwan': 2, 'hanyu': 3, 'korean': 4, 'dunhuang': 5}
    return list[name]
