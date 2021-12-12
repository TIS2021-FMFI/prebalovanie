from django.contrib.auth import get_user_model
from django.shortcuts import render

from repacking_site.methods import filtered_records
from .filters import *
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
    users_list_all = get_user_model().objects.all()
    users_filter = UserFilter(request.GET, queryset=users_list_all)
    paginate_by = request.GET.get('paginate_by', 10) or 10

    users_list = filtered_records(request, users_filter, paginate_by)
    context = {"users_list": users_list,
               'users_filter': users_filter, 'paginate_by': paginate_by}
    return render(request, 'accounts/user_list.html', context)
