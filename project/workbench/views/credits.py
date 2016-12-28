from django.shortcuts import render
from django.core.cache import cache
from django.contrib.auth.decorators import login_required


@login_required
def redeem_page(request):
    return render(request, 'credits_redeem.html')


@login_required
def details_page(request):
    return render(request, 'credits_details.html')


@login_required
def ranking_page(request):
    return render(request, 'credits_ranking.html')


@login_required
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
