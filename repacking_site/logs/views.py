from django.http import Http404, HttpResponseRedirect

from django.shortcuts import render

from logs.models import Log


def index(request):
    log_list = Log.filter_and_order_logs_by_get(request.GET)
    context = {"log_list": log_list}
    return render(request, 'logs/index.html', context)
