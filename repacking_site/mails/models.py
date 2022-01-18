import csv

import datetime
from io import StringIO

from django.core.mail import EmailMessage
from django.db import models

from repacking.models import RepackHistory


class MailSendSetting(models.Model):
    class Meta:
        verbose_name = 'Mailová adresa'
        verbose_name_plural = 'Mailové adresy'
        permissions = ()
        default_permissions = ()

    mail = models.EmailField(max_length=50, default="", verbose_name="Email")

    def __str__(self):
        return str(self.mail)

    @staticmethod
    def filter_and_order_emails_by_get(get):
        order_by = get.get('order_by', "-mail")
        try:
            if order_by[0] == '-':
                MailSendSetting._meta.get_field(order_by[1:])
            else:
                MailSendSetting._meta.get_field(order_by)
        except:
            order_by = "-mail"
        email_list = MailSendSetting.objects.filter(
            mail__contains=get.get('mail', ""),
        ).order_by(order_by)
        return email_list

    @staticmethod
    def get_mail(mail):
        try:
            standard = MailSendSetting.objects.get(mail=mail)
            return standard
        except MailSendSetting.DoesNotExist:
            return None

    @staticmethod
    def send_mails():
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

        email.send(fail_silently=False)

