# -*- coding:utf8 -*-
from django.shortcuts import render


def index(request):
    return render(request, 'forum.html')
