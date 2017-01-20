from __future__ import unicode_literals

from backend.utils import get_today_credits


def today_credits(request):
    counts = get_today_credits(request.user.id)
    return {"today_credits": counts if counts is not None else 0}
