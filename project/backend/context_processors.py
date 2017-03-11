# -*- coding:utf8 -*-
import json
from backend.utils import get_today_credits, get_lqhanzi_font_path, get_kaixinsong_font_path, get_tripitaka_unicode_font_path
from backend.enums import TASK_PACKAGE_STATUS_ENUM, TASK_STATUS_ENUM, BUSINESS_TYPE_ENUM, BUSINESS_STAGE_ENUM
from backend.models import BUSINESS_STAGE_CHOICES, BUSINESS_TYPE_CHOICES, INPUT_VARIANT_TYPE_CHOICES


def today_credits(request):
    counts = get_today_credits(request.user.id)
    return {"today_credits": counts if counts is not None else 0}


def model_enum(request):
    return {
        "task_package_status_enum": TASK_PACKAGE_STATUS_ENUM,
        "task_status_enum": TASK_STATUS_ENUM,
        "business_type_enum": BUSINESS_TYPE_ENUM,
        "business_stage_enum": BUSINESS_STAGE_ENUM,
        "business_type_choices": BUSINESS_TYPE_CHOICES,
        "business_stage_choices": BUSINESS_STAGE_CHOICES,
        "input_variant_type_choices": INPUT_VARIANT_TYPE_CHOICES,
        "business_type_choices_json": json.dumps(dict(BUSINESS_TYPE_CHOICES), encoding="UTF-8", ensure_ascii=False),
        "business_stage_choices_json": json.dumps(dict(BUSINESS_STAGE_CHOICES), encoding="UTF-8", ensure_ascii=False),
    }


def lqhanzi_font(request):
    return {
        'lqhanzi_font_path': get_lqhanzi_font_path(),
        'kaixinsong_font_path': get_kaixinsong_font_path(),
        'tripitaka_font_path': get_tripitaka_unicode_font_path(),
    }
