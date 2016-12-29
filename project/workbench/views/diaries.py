# -*- coding:utf8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import Context
from .credits import get_user_today_and_total_credits


@login_required
def index(request):
    c = Context()
    c.update(get_user_today_and_total_credits(request.user.id))
    return render(request, 'diaries.html', c)
