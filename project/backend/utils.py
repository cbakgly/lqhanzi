# -*- coding:utf8 -*-
from django.core.cache import cache

from backend.cache_keys import getcachekey_today_credits


def get_today_credits(user_id):
    key = getcachekey_today_credits(user_id)
    return cache.get(key, 0)
