# -*- coding:utf8 -*-
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.template import Context
import django_filters.rest_framework

from .. import wb_filter
from .credits import get_user_today_and_total_credits


@login_required
def index(request):
    c = Context()
    c.update(get_user_today_and_total_credits(request.user.id))
    return render(request, 'diaries.html', c)
