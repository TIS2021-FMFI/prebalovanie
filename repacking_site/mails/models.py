from django.db import models


class MailSendSetting(models.Model):
    class Meta:
        verbose_name = 'Mailová adresa'
        verbose_name_plural = 'Mailové adresy'

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
