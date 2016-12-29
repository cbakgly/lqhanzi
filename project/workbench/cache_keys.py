# -*- coding:utf8 -*-


# 集中列出所有m2中用到的缓存key
# 以getcachekey开头作为函数名称

def getcachekey_today_completed_task_num(user_id, business_type):
    return 'user:' + str(user_id) + ':num_of_today_completed_task:busi_type:' + str(business_type)


def getcachekey_today_credits(user_id):
    return 'user:' + str(user_id) + ':today_credits'

