import csv
from io import StringIO
from django.shortcuts import render
from django.core.mail import EmailMessage
from .models import *
import datetime

from repacking.models import RepackHistory


def index(request):
    email = EmailMessage(
        f'[GEFCO prebaľovanie] Report {datetime.datetime.now().strftime("%d.%m.%Y")} - '
        f'{(datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%d.%m.%Y")}',
        f'Dobrý deň,\nv prlohe tohoto mailu nájdete zoznam prebaľovaní za posledných 7 dní, teda od '
        f'{datetime.datetime.now().strftime("%d.%m.%Y")} do '
        f'{(datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%d.%m.%Y")}',
        'prebalovanie@gefcoslovakia.sk',
        [mail.mail for mail in MailSendSetting.objects.all()],
    )
    csvfile = StringIO()
    writer = csv.writer(csvfile, dialect='excel', delimiter=',')
    writer.writerow(['Čas začiatku prebalu', 'Čas konca prebalu', 'Čas prebalu', 'operátori',
                     'SKU', 'COFOR', 'Destinácia', 'ks IN', 'ks OUT',
                     'ks v obale IN', 'ks v obale OUT', 'boxy IN', 'boxy OUT',
                     'Trvanie prebalu podľa štandardu', 'kg/ks', 'vytvoril', 'Čas vytvorenia', 'Poznámka'])

    for repack in RepackHistory.objects.all():
        writer.writerow([repack.repack_start, repack.repack_finish, repack.repack_duration,
                         ', '.join(map(str, repack.users.all())),
                         repack.repacking_standard.SKU, repack.repacking_standard.COFOR,
                         repack.repacking_standard.destination,
                         repack.repacking_standard.input_count_of_items_on_pallet,
                         repack.repacking_standard.output_count_of_items_on_pallet,
                         repack.repacking_standard.input_count_of_items_in_package,
                         repack.repacking_standard.output_count_of_items_in_package,
                         repack.repacking_standard.input_count_of_boxes_on_pallet,
                         repack.repacking_standard.output_count_of_boxes_on_pallet,
                         repack.repacking_standard.repacking_duration,
                         repack.repacking_standard.unit_weight, repack.repacking_standard.creator,
                         repack.repacking_standard.created, repack.repacking_standard.instructions])
    email.attach('text.csv', csvfile.getvalue(), 'text/csv')
    email.send(fail_silently=False)
    return render(request, 'mails/index.html')
