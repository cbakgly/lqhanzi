from django.shortcuts import render


def redeem_page(request):
    return render(request, 'credits_redeem.html')


def details_page(request):
    return render(request, 'credits_details.html')


def ranking_page(request):
    return render(request, 'credits_ranking.html')
