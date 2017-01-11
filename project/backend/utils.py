from django.core.cache import cache

from backend.cache_keys import getcachekey_today_credits
from lqconfig.settings import STATIC_URL, USE_S3_HANZI_PICTURE


def get_today_credits(user_id):
    key = getcachekey_today_credits(user_id)
    return cache.get(key, 0)


def get_hanzi_assets_path():
    if not USE_S3_HANZI_PICTURE:
        return STATIC_URL + 'img/'
    else:
        return 'http://s3.cn-north-1.amazonaws.com.cn/lqhanzi-images/'


def get_dunhuang_dict_path():
    return get_hanzi_assets_path() + ('dictionaries/dh-dict/')


def get_hanyu_dict_path():
    return get_hanzi_assets_path() + ('dictionaries/zh-dict/')


def get_hanzi_parts_path():
    return get_hanzi_assets_path() + ('components/')


def get_dunhuang_char_pic_path(pic_name):
    return get_hanzi_assets_path() + 'glyphs/dh/standard/' + pic_name + '.png'


def get_korean_char_pic_path(pic_name):
    code = int(pic_name[-1]) if pic_name else 0
    switcher = {
        0: lambda: "glyphs/gl/standard/",
        1: lambda: "glyphs/gl/variant1/",
        2: lambda: "glyphs/gl/variant2/",
    }
    mid_path = switcher.get(code, lambda x: "")
    return get_hanzi_assets_path() + mid_path() + pic_name + '.png'


def get_hanyu_char_pic_path(pic_name):
    return get_hanzi_assets_path() + 'glyphs/hy/' + pic_name + '.png'


def get_taiwan_char_pic_path(pic_name):
    return get_hanzi_assets_path() + 'glyphs/tw/' + pic_name[:2] + '/' + pic_name + '.png' if len(pic_name) <= 2 else ''


def get_pic_url_by_source_pic_name(source, pic_name):
    if not pic_name:
        return ""

    switcher = {
        2: get_taiwan_char_pic_path,
        3: get_hanyu_char_pic_path,
        4: get_korean_char_pic_path,
        5: get_dunhuang_char_pic_path
    }

    func = switcher.get(source, lambda name: "")
    return func(pic_name)
