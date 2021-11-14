from django.db import models


class MailSendSetting(models.Model):
    mail = models.EmailField(max_length=50, default="")
