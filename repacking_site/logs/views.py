from django.http import Http404, HttpResponseRedirect

from django.shortcuts import render

from logs.models import Log


def index(request): #tu
     log_list = Log.objects.all()
     context = {"log_list": log_list}
     return render(request, 'logs/index.html', context)
