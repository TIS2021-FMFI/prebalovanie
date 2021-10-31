from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from .models import *
from .forms import *


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


def make_new_standard(request):
    if request.method == 'POST':
        form = RepackingStandardForm(request.POST)
        if form.is_valid():
            RepackingStandard(
                SKU_code=form.cleaned_data['SKU_code'],
                COFOR_code=form.cleaned_data['COFOR_code'],
                supplier=form.cleaned_data['supplier'],
                destination=form.cleaned_data['destination'],
                pcs_per_move=form.cleaned_data['pcs_per_move'],
                unit_weight=form.cleaned_data['unit_weight'],
                repacking_time=datetime.timedelta(seconds=form.cleaned_data['repacking_time']),
                remark=form.cleaned_data['remark'],
                pcs_package_in=form.cleaned_data['pcs_package_in'],
                pcs_package_out=form.cleaned_data['pcs_package_out'],
                boxes_on_pallet_in=form.cleaned_data['boxes_on_pallet_in'],
                boxes_on_pallet_out=form.cleaned_data['boxes_on_pallet_out'],
                pcs_on_pallet_in=form.cleaned_data['pcs_on_pallet_in'],
                pcs_on_pallet_out=form.cleaned_data['pcs_on_pallet_out'],
                package_type_in=form.cleaned_data['package_type_in'],
                package_type_out=form.cleaned_data['package_type_out']
            ).save()

            return HttpResponseRedirect("/")

    else:
        form = RepackingStandardForm()

    return render(request, 'repacking/new_standard.html', {'form': form})
