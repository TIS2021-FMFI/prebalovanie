import csv

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render

from repacking_site.methods import filtered_records
from .filters import *


@permission_required('accounts.user_managment')
@login_required
def index(request):
    log_list_all = Log.filter_and_order_logs_by_get(request.GET)
    log_filter = LogFilter(request.GET, queryset=log_list_all)
    filter_GET = request.GET.copy()
    if "paginate_by" in filter_GET:
        filter_GET.pop("paginate_by")
    if "page" in filter_GET:
        filter_GET.pop("page")
    if len(filter_GET) != 0:
        filter_GET_code = "&" + filter_GET.urlencode()
    else:
        filter_GET_code = ""
    paginate_by = request.GET.get('paginate_by', 10) or 10
    open_filter = False
    if request.GET.get("paginate_by") is None and request.GET.get("page") is None and len(request.GET.keys()) != 0:
        open_filter = True
    if request.GET.get("paginate_by") is not None and request.GET.get("page") is not None and len(
            request.GET.keys()) > 2:
        open_filter = True
    if len(request.GET.keys()) > 1:
        if request.GET.get("paginate_by") is not None and request.GET.get("page") is None:
            open_filter = True
        if request.GET.get("paginate_by") is None and request.GET.get("page") is not None:
            open_filter = True
    log_list = filtered_records(request, log_filter, paginate_by)
    context = {"log_list": log_list,
               'log_filter': log_filter, 'paginate_by': paginate_by, 'open_filter': open_filter,
               "filter_GET": filter_GET_code}
    return render(request, 'logs/index.html', context)


@permission_required('accounts.user_managment')
@login_required
def logs_export(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="logs-export.csv"'},
    )

    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, dialect='excel', delimiter=';')
    Log.write_logs_to_csv(Log.objects.all(), writer)
    return response
