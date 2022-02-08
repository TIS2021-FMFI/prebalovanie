from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from logs.models import Log
from repacking_site.methods import filtered_records
from .filters import *
from .forms import *


@permission_required('accounts.history')
@login_required
def index(request):
    if request.method == 'POST' and 'add_mail' in request.POST:
        form = AddEmailForm(request.POST)
        if form.is_valid():
            if MailSendSetting.get_mail(form.cleaned_data['email']) is not None:
                raise FileExistsError("Email address already exists")

            mail_form = MailSendSetting(
                mail=form.cleaned_data['email']
            )
            mail_form.save()

            Log.make_log(Log.App.MAIL_REPORTS, Log.Priority.DEBUG, request.user, "Pridaná mailová adresa")

            return HttpResponseRedirect("/mails/index/")
    else:
        mail_form = AddEmailForm()

    email_list_all = MailSendSetting.filter_and_order_emails_by_get(request.GET)
    email_list_filter = EmailListFilter(request.GET, queryset=email_list_all)
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

    email_list = filtered_records(request, email_list_filter, paginate_by)
    context = {"email_list": email_list,
               'email_list_filter': email_list_filter, 'paginate_by': paginate_by, "open_filter": open_filter,
               "filter_GET": filter_GET_code, "add_email_form": mail_form, "update_date_form": None}
    return render(request, 'mails/index.html', context)


@permission_required('accounts.sku_managment')
@login_required
def delete(request, mail):
    email = MailSendSetting.get_mail(mail)
    if email is None:
        deleted = False
    else:
        email.delete()
        deleted = True
    return render(request, 'mails/email_deleted.html', {'deleted': deleted})


def send(request):
    MailSendSetting.send_mails()

    return render(request, 'mails/sent.html')
