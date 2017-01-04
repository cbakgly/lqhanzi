# -*- coding:utf8 -*-
from django.core.cache import cache

from backend.cache_keys import getcachekey_today_credits


def get_today_credits(user_id):
    key = getcachekey_today_credits(user_id)
    return cache.get(key, 0)


def get_source_path_mapping(source):
    pass


def get_hanzi_assets_path():
    return 'lqhanzi-assets/image/'


def get_dunhuang_dict_path():
    return get_hanzi_assets_path().join('dictionaries/dh-dict/')


def get_hanyu_dict_path():
    return get_hanzi_assets_path().join('dictionaries/zh-dict/')


def get_hanzi_parts_path():
    return get_hanzi_assets_path().join('hanzi-parts/')


def get_dunhuang_char_pic_path():
    return get_hanzi_assets_path().join('hanzi-pictures/dh/standard/')


def get_korean_char_pic_path():
    return get_hanzi_assets_path().join('hanzi-pictures/gl/')


def get_hanyu_char_pic_path():
    return get_hanzi_assets_path().join('hanzi-pictures/hy/')
