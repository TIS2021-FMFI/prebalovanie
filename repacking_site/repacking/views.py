from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from .models import *
from .forms import *

from logs.models import Log


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
    repackings_list = RepackHistory.objects.all()
    context = {"repackings_list": repackings_list}
    return render(request, 'repacking/history.html', context)


def finish(request, sku_code):
    standard = RepackingStandard.get_repacking_standard_by_sku(sku_code)
    if standard is None:
        raise Http404("Standard does not exist")

    repack = RepackHistory(repacking_standard=standard, idp=0)
    repack.save()

    Log.make_log(Log.App.REPACKING, Log.Priority.DEBUG, None, "Repack finished")

    return index(request)


def make_new_standard(request):
    if request.method == 'POST':
        form = RepackingStandardForm(request.POST)
        if form.is_valid() and form.cleaned_data['repacking_duration'] is not None:
            if RepackingStandard.get_repacking_standard_by_sku(form.cleaned_data['SKU']) is not None:
                raise FileExistsError("Repacking standard w/ this SKU already exists")
            RepackingStandard(
                SKU=form.cleaned_data['SKU'],
                COFOR=form.cleaned_data['COFOR'],
                supplier=form.cleaned_data['supplier'],
                destination=form.cleaned_data['destination'],
                items_per_move=form.cleaned_data['items_per_move'],
                unit_weight=form.cleaned_data['unit_weight'],
                repacking_duration=datetime.timedelta(seconds=form.cleaned_data['repacking_duration']),
                instructions=form.cleaned_data['instructions'],
                input_count_of_items_in_package=form.cleaned_data['input_count_of_items_in_package'],
                output_count_of_items_in_package=form.cleaned_data['output_count_of_items_in_package'],
                input_count_of_boxes_on_pallet=form.cleaned_data['input_count_of_boxes_on_pallet'],
                output_count_of_boxes_on_pallet=form.cleaned_data['output_count_of_boxes_on_pallet'],
                input_count_of_items_on_pallet=form.cleaned_data['input_count_of_items_on_pallet'],
                output_count_of_items_on_pallet=form.cleaned_data['output_count_of_items_on_pallet'],
                input_type_of_package=form.cleaned_data['input_type_of_package'],
                output_type_of_package=form.cleaned_data['output_type_of_package']
            ).save()

            Log.make_log(Log.App.REPACKING, Log.Priority.DEBUG, None, "Repacking standard made")

            return HttpResponseRedirect("/")

    else:
        form = RepackingStandardForm()

    return render(request, 'repacking/new_standard.html', {'form': form})
