import csv
from io import StringIO
from django.shortcuts import render
from django.core.mail import EmailMessage
from .models import *
from repacking.models import *
import datetime

from repacking.models import RepackHistory


def index(request):
    email = EmailMessage(
        f'[GEFCO prebaľovanie] Report '
        f'{(datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%d.%m.%Y")} - '
        f'{datetime.datetime.now().strftime("%d.%m.%Y")}',
        f'Dobrý deň,\nv prlohe tohoto mailu nájdete zoznam prebaľovaní za posledných 7 dní, teda od '
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
    email.send(fail_silently=False)
    return render(request, 'mails/index.html')
