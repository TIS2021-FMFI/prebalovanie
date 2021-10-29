from django.http import HttpResponse, Http404
from django.shortcuts import render

from .models import *


def index(request):
    repacking_list = RepackingStandard.objects.all()
    context = {"repacking_list": repacking_list}
    return render(request, 'repacking/index.html', context)


def detail(request, sku_code):
    try:
        standard = RepackingStandard.objects.get(SKU_code=sku_code)
    except RepackingStandard.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'repacking/detail.html', {'standard': standard})
