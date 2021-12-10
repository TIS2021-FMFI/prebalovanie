from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from employees.models import *
from logs.models import Log
from .filters import *
from .forms import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

repack_start_key = 'repack_start'
repack_last_start_key = 'repack_last_start'
repack_duration_key = 'repack_duration'
repack_time_format = '%Y-%m-%dT%H:%M:%S'


def index(request):
    cancel_sessions(request)
    return render(request, 'repacking/index.html')


def repacking(request, sku_code, idp_code, operators):
    standard = RepackingStandard.get_repacking_standard_by_sku(sku_code)
    if standard is None:
        raise Http404("Standard does not exist")

    if request.session.get(repack_start_key, None) is None:
        request.session[repack_start_key] = datetime.now().strftime(repack_time_format)
        request.session[repack_duration_key] = 0
    request.session[repack_last_start_key] = datetime.now().strftime(repack_time_format)

    return render(request, 'repacking/repack.html', {'standard': standard, 'idp': idp_code, 'operators': operators})


def detail(request, sku_code):
    cancel_sessions(request)
    standard = RepackingStandard.get_repacking_standard_by_sku(sku_code)
    if standard is None:
        raise Http404("Standard does not exist")
    return render(request, 'repacking/detail.html', {'standard': standard})


def history(request):
    cancel_sessions(request)
    repackings_list = RepackHistory.filter_and_order_repacking_history_by_get(request.GET)
    context = {"repackings_list": repackings_list}
    return render(request, 'repacking/history.html', context)


def start(request):
    cancel_sessions(request)
    if request.method == 'POST':
        form = RepackingForm(request.POST)
        if form.is_valid():
            if RepackingStandard.get_repacking_standard_by_sku(form.cleaned_data['SKU']) is None:
                raise FileExistsError("RepackingForm standard w/ this SKU does not exists")

            operators = set()
            i = 1
            while f'operator_{i}' in request.POST.keys():
                operator = request.POST[f'operator_{i}']
                if operator != '':
                    User.objects.get(barcode=operator)
                    operators.add(operator)
                i += 1

            return HttpResponseRedirect(
                f'/repacking/{form.cleaned_data["SKU"]}/{form.cleaned_data["IDP"]}/{",".join(operators)}/')

    else:
        form = RepackingForm()

    return render(request, 'repacking/start.html', {'form': form})


def show_standards(request):
    cancel_sessions(request)
    repacking_standards_list_all = RepackingStandard.filter_and_order_repacking_standard_by_get(request.GET)
    # inspiracia: https://www.youtube.com/watch?v=G-Rct7Na0UQ
    standards_filter = RepackingStandardFilter(request.GET, queryset=repacking_standards_list_all)
    repacking_standards_list_filtered = standards_filter.queryset

    # paginacia  https://www.youtube.com/watch?v=N-PB-HMFmdo
    # pocet udajov na stranke https://stackoverflow.com/questions/57487336/change-value-for-paginate-by-on-the-fly
    paginate_by = request.GET.get('paginate_by', 10) or 10
    p = Paginator(repacking_standards_list_filtered, paginate_by)
    page = request.GET.get('page')

    try:
        repacking_standards_list = p.get_page(page)
    except PageNotAnInteger:
        repacking_standards_list = p.get_page(1)
    except EmptyPage:
        repacking_standards_list = p.get_page(1)

    context = {"repacking_standards_list": repacking_standards_list,
               'standards_filter': standards_filter, 'paginate_by': paginate_by}
    return render(request, 'repacking/standards.html', context)


def finish(request, sku_code, idp_code, operators):
    standard = RepackingStandard.get_repacking_standard_by_sku(sku_code)
    if standard is None:
        raise Http404("Standard does not exist")

    Log.make_log(Log.App.REPACKING, Log.Priority.DEBUG, None, "Repack finished")

    repack_finish = datetime.now()
    repack = RepackHistory(repacking_standard=standard, idp=idp_code, repack_finish=repack_finish)
    if request.session.get(repack_start_key, False):
        repack.repack_start = request.session.get(repack_start_key)
        last_repack_start = request.session.get(repack_last_start_key)
        repack_duration = request.session.get(repack_duration_key) + (
                datetime.now() - datetime.strptime(last_repack_start,
                                                   repack_time_format)).total_seconds()
        repack.repack_duration = timedelta(seconds=repack_duration)

    else:
        Log.make_log(Log.App.REPACKING, Log.Priority.ERROR, None, "RepackingForm without session finished.")

    cancel_sessions(request)

    repack.save()

    for operator in operators.split(','):
        repack.users.add(User.objects.get(barcode=operator))

    return HttpResponseRedirect('/repacking/start/')


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


def cancel(request, sku_code, idp_code, operators):
    cancel_sessions(request)
    return HttpResponseRedirect('/repacking/')


def pause(request, sku_code, idp_code, operators):
    repack_paused = datetime.now()
    if request.session.get(repack_duration_key, None) is not None:
        last_repack_start = request.session.get(repack_last_start_key)
        request.session[repack_duration_key] = request.session.get(repack_duration_key) + (
                repack_paused - datetime.strptime(last_repack_start, repack_time_format)).total_seconds()

    else:
        Log.make_log(Log.App.REPACKING, Log.Priority.ERROR, None, "RepackingForm without session saved.")

    context = {'sku_code': sku_code, 'idp_code': idp_code, 'operators': operators}
    return render(request, 'repacking/pause.html', context)


def make_new_standard(request):
    cancel_sessions(request)
    if request.method == 'POST':
        form = RepackingStandardForm(request.POST, request.FILES)
        if form.is_valid() and form.cleaned_data['repacking_duration'] is not None:
            if RepackingStandard.get_repacking_standard_by_sku(form.cleaned_data['SKU']) is not None:
                raise FileExistsError("RepackingForm standard w/ this SKU already exists")

            standard = RepackingStandard(
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
            )
            standard.save()

            if 'input_photos' in form.files:
                for photo in form.files.getlist('input_photos'):
                    input_photo = Photos(photo=photo)
                    input_photo.save()
                    standard.input_photos.add(input_photo)
            if 'output_photos' in form.files:
                for photo in form.files.getlist('output_photos'):
                    output_photo = Photos(photo=photo)
                    output_photo.save()
                    standard.output_photos.add(output_photo)
            if 'tools' in form.files:
                for photo in form.files.getlist('tools'):
                    tool = Tools(photo=photo)
                    tool.save()
                    standard.tools.add(tool)

            Log.make_log(Log.App.REPACKING, Log.Priority.DEBUG, None, "RepackingForm standard made")

            return HttpResponseRedirect("/")

    else:
        form = RepackingStandardForm()

    return render(request, 'repacking/new_standard.html', {'form': form})
