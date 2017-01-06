# -*- coding:utf8 -*-

# 集中将业务上的枚举类型的工具函数写在这里


def getenum_business_status(name):
    status = {"ongoing": 0, "completed": 1}
    return status[name]


def getenum_business_type(name):
    type = {"input": 0, "split": 1, "dedup": 2, "help": 3}
    return type[name]


def getenum_source(name):
    list = {'unicode': 1, 'tw': 2, 'hy': 3, 'gl': 4, 'dh': 5}
    return list[name]
