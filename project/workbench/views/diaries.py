# -*- coding:utf8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from backend.utils import has_workbench_perm


@login_required
def index(request):
    if has_workbench_perm(request.user):
        return render(request, 'diaries.html')
    return render(request, '401.html')
