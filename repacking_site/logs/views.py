from django.shortcuts import render

from repacking_site.methods import filtered_records
from .filters import *


def index(request):
    log_list_all = Log.filter_and_order_logs_by_get(request.GET)
    log_filter = LogFilter(request.GET, queryset=log_list_all)
    paginate_by = request.GET.get('paginate_by', 10) or 10
    open_filter = False
    if request.GET.get("paginate_by") is None and request.GET.get("page") is None and len(request.GET.keys()) != 0:
        open_filter = True
    elif request.GET.get("paginate_by") is not None and request.GET.get("page") is not None and len(
            request.GET.keys()) > 2:
        open_filter = True
    elif request.GET.get("paginate_by") is not None and request.GET.get("page") is not None and len(
            request.GET.keys()) > 1:
        open_filter = True
    log_list = filtered_records(request, log_filter, paginate_by)
    context = {"log_list": log_list,
               'log_filter': log_filter, 'paginate_by': paginate_by, 'open_filter': open_filter}
    return render(request, 'logs/index.html', context)
