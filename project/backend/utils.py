from django.core.cache import cache

from backend.cache_keys import getcachekey_today_credits
from lqconfig.settings import STATIC_URL


def get_today_credits(user_id):
    key = getcachekey_today_credits(user_id)
    return cache.get(key, 0)


def get_source_path_mapping(source):
    pass


def get_hanzi_assets_path():
    return STATIC_URL + 'img/'


def get_dunhuang_dict_path():
    return get_hanzi_assets_path() + ('dictionaries/dh-dict/')


def get_hanyu_dict_path():
    return get_hanzi_assets_path() + ('dictionaries/zh-dict/')


def get_hanzi_parts_path():
    return get_hanzi_assets_path() + ('components/')


def get_dunhuang_char_pic_path():
    return get_hanzi_assets_path() + ('glyphs/dh/standard/')


def get_korean_char_pic_path():
    return get_hanzi_assets_path() + ('glyphs/gl/')


def get_korean_char_pic_std_path():
    return get_hanzi_assets_path() + ('glyphs/gl/standard/')


def get_korean_char_pic_variant_path(id):
    return get_hanzi_assets_path() + ('glyphs/gl/variant') + str(id) + '/'


def get_hanyu_char_pic_path():
    return get_hanzi_assets_path() + ('glyphs/hy/')


def get_taiwan_char_pic_path():
    return get_hanzi_assets_path() + ('glyphs/tw/')
