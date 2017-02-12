from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from backend.utils import has_workbench_perm


@login_required
def redeem_page(request):
    if has_workbench_perm(request.user):
        return render(request, 'credits_redeem.html')
    return render(request, '401.html')


@login_required
def details_page(request):
    if has_workbench_perm(request.user):
        return render(request, 'credits_details.html')
    return render(request, '401.html')


@login_required
def ranking_page(request):
    if has_workbench_perm(request.user):
        return render(request, 'credits_ranking.html')
    return render(request, '401.html')
