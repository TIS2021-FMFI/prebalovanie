from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from .models import *
from .forms import *

from logs.models import Log

repack_start_key = 'repack_start'
repack_last_start_key = 'repack_last_start'
repack_duration_key = 'repack_duration'
repack_time_format = '%Y-%m-%dT%H:%M:%S'

def index(request):
    cancel_sessions(request)
    repacking_standards_list = RepackingStandard.objects.all()
    context = {"repacking_standards_list": repacking_standards_list}
    return render(request, 'repacking/index.html', context)


def detail(request, sku_code):
    standard = RepackingStandard.get_repacking_standard_by_sku(sku_code)
    if standard is None:
        raise Http404("Standard does not exist")
    if request.session.get(repack_start_key, None) is None:
        request.session[repack_start_key] = datetime.now().strftime(repack_time_format)
        request.session[repack_duration_key] = 0
    request.session[repack_last_start_key] = datetime.now().strftime(repack_time_format)
    return render(request, 'repacking/detail.html', {'standard': standard})


def history(request):
    repackings_list = RepackHistory.objects.all()
    context = {"repackings_list": repackings_list}
    return render(request, 'repacking/history.html', context)


def finish(request, sku_code):
    standard = RepackingStandard.get_repacking_standard_by_sku(sku_code)
    if standard is None:
        raise Http404("Standard does not exist")

    Log.make_log(Log.App.REPACKING, Log.Priority.DEBUG, None, "Repack finished")

    repack_finish = datetime.now()
    repack = RepackHistory(repacking_standard=standard, idp=0, repack_finish=repack_finish)
    if request.session.get(repack_start_key, False):
        repack.repack_start = request.session.get(repack_start_key)
        last_repack_start = request.session.get(repack_last_start_key)
        repack_duration = request.session.get(repack_duration_key) + (
                    datetime.now() - datetime.strptime(last_repack_start,
                                                       repack_time_format)).total_seconds()
        repack.repack_duration = timedelta(seconds=repack_duration)

    else:
        # TODO logging
        ...

    cancel_sessions(request)

    repack.save()
    return HttpResponseRedirect('/repacking/')


def cancel_sessions(request):
    try:
        del request.session[repack_start_key]
    except KeyError:
        pass

    try:
        del request.session[repack_last_start_key]
    except KeyError:
        pass

    try:
        del request.session[repack_duration_key]
    except KeyError:
        pass


def cancel(request, sku_code):
    cancel_sessions(request)

    return HttpResponseRedirect('/repacking/')


def pause(request, sku_code):
    repack_paused = datetime.now()
    if request.session.get(repack_duration_key, None) is not None:
        last_repack_start = request.session.get(repack_last_start_key)
        request.session[repack_duration_key] = request.session.get(repack_duration_key) + \
                                               (repack_paused - datetime.strptime(last_repack_start,
                                                                                  repack_time_format)).total_seconds()
        
    else:
        # TODO logging
        ...
    context = {'sku_code': sku_code}
    return render(request, 'repacking/pause.html', context)


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
                repacking_duration=timedelta(seconds=form.cleaned_data['repacking_duration']),
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
