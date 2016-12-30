from django.shortcuts import render
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
