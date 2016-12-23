from django.shortcuts import render
from django.db.models import Sum
from django.core.cache import cache

from ..models import Credits


def redeem_page(request):
    return render(request, 'credits_redeem.html')


def details_page(request):
    return render(request, 'credits_details.html')


def ranking_page(request):
    return render(request, 'credits_ranking.html')


def get_user_today_and_total_credits(user_id):
    # dat = Credits.objects.filter(user_id=user_id)
    # total_credits = dat.aggregate(Sum('credit'))
    # today_credits = dat.filter()
    today_credits = cache.get('m2.today_credits'.join(str(user_id)))
    total_credits = cache.get('m2.total_credits'.join(str(user_id)))
    return {
        "today_credits": today_credits,
        "total_credits": total_credits
    }
