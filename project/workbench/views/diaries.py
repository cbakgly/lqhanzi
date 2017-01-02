# -*- coding:utf8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from backend.utils import get_today_credits


@login_required
def index(request):
    today_credits = get_today_credits(request.user.id)
    return render(request, 'diaries.html', {"today_credits": today_credits})
