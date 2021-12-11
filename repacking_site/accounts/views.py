from django.http import Http404, HttpResponseRedirect

from django.shortcuts import render
from django.contrib.auth import get_user_model

from .forms import *


def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            if request.user.is_authenticated:
                request.user.first_name = form.cleaned_data['first_name']
                request.user.last_name = form.cleaned_data['last_name']
                request.user.save()
            return render(request, 'accounts/profile.html', {'form': form})

    else:
        form = ProfileForm({'first_name': request.user.first_name, 'last_name': request.user.last_name})
        return render(request, 'accounts/profile.html', {'form': form})


def user_list(request):
    return render(request, 'accounts/user_list.html', {'users': get_user_model().objects.all()})
