from django.http import Http404, HttpResponseRedirect

from django.shortcuts import render

from logs.models import Log


def profile(request):
    return render(request, 'accounts/index.html')
