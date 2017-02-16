from datetime import date, datetime
from django.db.models import Sum, Count
from django.utils import timezone

from lqconfig.settings import STATIC_URL, USE_S3_HANZI_PICTURE
from functional import timeout_cache
from models import Tasks
from enums import PERMS


# https://docs.djangoproject.com/en/dev/topics/i18n/timezones/#selecting-the-current-time-zone
# see above to learn timezone usage

# 5 minutes
@timeout_cache(5 * 60)
def get_today_credits(user_id):
    today = date.today()
    start = datetime(today.year, today.month, today.day, tzinfo=timezone.utc)
    end = start + timezone.timedelta(days=1)
    ret = Tasks.objects.filter(user_id=user_id).filter(completed_at__range=(start, end)).values("credits").aggregate(Sum("credits"))
    return ret['credits__sum']


@timeout_cache(5 * 60)
def get_today_complete_task_num(user_id, business_type):
    today = date.today()
    start = timezone.make_aware(datetime(today.year, today.month, today.day, 0, 0, 0), timezone.get_current_timezone())
    end = start + timezone.timedelta(days=1)
    ret = Tasks.objects.filter(user_id=user_id).filter(business_type=business_type).filter(completed_at__range=(start, end)).values("id").aggregate(Count("id"))
    return ret['id__count']


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
    try:
        code = int(pic_name[-1])
    except Exception:
        code = 0

    switcher = {
        0: lambda: "glyphs/gl/standard/",
        1: lambda: "glyphs/gl/variant1/",
        2: lambda: "glyphs/gl/variant2/",
    }
    mid_path = switcher.get(code, lambda x: "")

    if code == 0:
        pic_name = 'kr' + pic_name + '0'
    return get_hanzi_assets_path() + mid_path() + pic_name + '.png'


def get_hanyu_char_pic_path(pic_name):
    return get_hanzi_assets_path() + 'glyphs/hy/' + pic_name + '.png'


def get_taiwan_char_pic_path(pic_name):
    return get_hanzi_assets_path() + 'glyphs/tw/' + pic_name[:2] + '/' + pic_name + '.png' if len(pic_name) >= 2 else ''


def get_pic_url_by_source_pic_name(source, pic_name):
    if not pic_name:
        return ""

    switcher = {
        2: get_taiwan_char_pic_path,
        3: get_hanyu_char_pic_path,
        4: get_korean_char_pic_path,
        5: get_dunhuang_char_pic_path
    }

    func = switcher.get(int(source), lambda name: "")
    return func(pic_name)


def is_search_request(search_param, *keywords):
    for key in keywords:
        ret = search_param.get(key, False)
        if ret:
            return True
    return False


def is_int(n):
    try:
        int(n)
        return True
    except Exception:
        return False


def has_workbench_perm(user):
    user_perms = user.get_group_permissions()
    perms = PERMS.values()
    for p in user_perms:
        if p in perms:
            return True
    return False


def has_business_type_perm(user, type):
    split_perms = [p for p in PERMS.values() if p.find(type) != -1]
    for p in split_perms:
        if user.has_perm(p):
            return True
    return False


def get_lqhanzi_font_path():
    return 'http://s3.cn-north-1.amazonaws.com.cn/lqhanzi-misc/fonts/lqhanzi.ttf'
