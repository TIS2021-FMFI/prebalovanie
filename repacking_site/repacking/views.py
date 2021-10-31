from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    repacking_standards_list = RepackingStandard.objects.all()
    context = {"repacking_standards_list": repacking_standards_list}
    return render(request, 'repacking/index.html', context)


def detail(request, sku_code):
    standard = RepackingStandard.get_repacking_standard_by_sku(sku_code)
    if standard is None:
        raise Http404("Standard does not exist")
    return render(request, 'repacking/detail.html', {'standard': standard})


def history(request):
    repackings_list = Repack.objects.all()
    context = {"repackings_list": repackings_list}
    return render(request, 'repacking/history.html', context)


def finish(request, sku_code):
    standard = RepackingStandard.get_repacking_standard_by_sku(sku_code)
    if standard is None:
        raise Http404("Standard does not exist")

    repack = Repack(repacking_standard=standard, idp=0)
    repack.save()
    return index(request)

