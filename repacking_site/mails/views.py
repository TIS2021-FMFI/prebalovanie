import csv
from io import StringIO
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from .models import *
from repacking.models import *
import datetime

from repacking.models import RepackHistory

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse

from accounts.models import *
from logs.models import Log
from repacking_site.methods import filtered_records
from .filters import *
from .forms import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

@login_required
def index(request):
    email = EmailMessage(
        f'[GEFCO prebaľovanie] Report '
        f'{(datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%d.%m.%Y")} - '
        f'{datetime.datetime.now().strftime("%d.%m.%Y")}',
        f'Dobrý deň,\nv prílohe tohoto mailu nájdete zoznam prebaľovaní za posledných 7 dní, teda od '
        f'{(datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%d.%m.%Y")} do '
        f'{datetime.datetime.now().strftime("%d.%m.%Y")}',
        'prebalovanie@gefcoslovakia.sk',
        [mail.mail for mail in MailSendSetting.objects.all()],
    )
    csvfile = StringIO()
    writer = csv.writer(csvfile, dialect='excel', delimiter=',')

    RepackHistory.write_repacking_history_to_csv(RepackHistory.objects.filter(
        repack_finish__gte=(datetime.datetime.now() - datetime.timedelta(days=7))), writer)

    email.attach(f'prebalovania-{(datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y/%m/%d")}-'
                 f'{datetime.datetime.now().strftime("%Y/%m/%d")}', csvfile.getvalue(),
                 'text/csv')
    #email.send(fail_silently=False)

    ##---------------------------##

    if request.method == 'POST' and 'add_mail' in request.POST:
        form = AddEmailForm(request.POST)
        if form.is_valid():
            if MailSendSetting.get_mail(form.cleaned_data['email']) is not None:
                raise FileExistsError("Email address already exists")

            mail_form = MailSendSetting(
                mail=form.cleaned_data['email']
            )
            mail_form.save()

            Log.make_log(Log.App.MAIL_REPORTS, Log.Priority.DEBUG, None, "Added Email address")

            return HttpResponseRedirect("/mails/index/")
    else:
        mail_form = AddEmailForm()
    if request.method == 'POST' and 'add_mail' in request.POST:
        form = ExportUpdateForm(request.POST)
        if form.is_valid():

            # To be finished...

            #time_form = ...
            #time_form.save()

            #Log.make_log(Log.App.MAIL_REPORTS, Log.Priority.DEBUG, None, "Changed time of Updates")

            return HttpResponseRedirect("/mails/index/")
    else:
        date_form = ExportUpdateForm()

    ##----------------------------------##

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
               "filter_GET": filter_GET_code, "add_email_form": mail_form, "update_date_form": date_form}
    return render(request, 'mails/index.html', context)

@login_required
def delete(request, mail):
    email = MailSendSetting.get_mail(mail)
    if email is None:
        deleted = False
    else:
        email.delete()
        deleted = True
    return render(request, 'mails/email_deleted.html', {'deleted': deleted})
