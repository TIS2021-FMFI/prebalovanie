from django.shortcuts import render

from repacking_site.methods import filtered_records
from .filters import *


def index(request):
    log_list_all = Log.filter_and_order_logs_by_get(request.GET)
    log_filter = LogFilter(request.GET, queryset=log_list_all)
    paginate_by = request.GET.get('paginate_by', 10) or 10

    log_list = filtered_records(request, log_filter, paginate_by)
    context = {"log_list": log_list,
               'log_filter': log_filter, 'paginate_by': paginate_by}
    return render(request, 'logs/index.html', context)
