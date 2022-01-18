import csv

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render

from repacking_site.methods import filtered_records
from .filters import *
from .forms import *


@login_required
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
        if request.user.is_authenticated:
            form = ProfileForm({'first_name': request.user.first_name, 'last_name': request.user.last_name})
        else:
            form = ProfileForm()
        return render(request, 'accounts/profile.html', {'form': form})


@permission_required('accounts.user_managment')
@login_required
def export_users(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="users-export.csv"'},
    )

    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, dialect='excel', delimiter=';')
    writer.writerow(['Username', 'First name', 'Last name', 'Email', 'Is staff', 'Is active', 'Is superuser',
                     'groups', 'barcode'])
    for user in User.objects.all():
        writer.writerow([user.username, user.first_name, user.last_name, user.email,
                         user.is_staff, user.is_active, user.is_superuser,
                         ', '.join(map(str, user.groups.all())), repr(user.barcode)])
    return response


@permission_required('accounts.user_managment')
@login_required
def export_groups(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="users-export.csv"'},
    )

    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, dialect='excel', delimiter=';')
    writer.writerow(['Group name', 'Permissions'])
    for group in Group.objects.all():
        writer.writerow([group.name, ", ".join(map(str, group.permissions.all()))])
    return response


@permission_required('accounts.user_managment')
@login_required
def users_list(request):
    users_list_all = get_user_model().objects.all()
    users_filter = UserFilter(request.GET, queryset=users_list_all)
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
    users_list = filtered_records(request, users_filter, paginate_by)
    context = {"users_list": users_list,
               'users_filter': users_filter, 'paginate_by': paginate_by,
               'open_filter': open_filter, "filter_GET": filter_GET_code}
    return render(request, 'accounts/users_list.html', context)


@permission_required('accounts.user_managment')
@login_required
def groups_list(request):
    return render(request, 'accounts/groups_list.html', {'groups': Group.objects.all()})
