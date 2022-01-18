from django.db import models
from django.conf import settings


class Log(models.Model):
    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logy'
        permissions = ()
        default_permissions = ()

    class Priority(models.TextChoices):
        TRACE = 'TRACE'
        DEBUG = 'DEBUG'
        INFO = 'INFO'
        WARNING = 'WARNING'
        ERROR = 'ERROR'
        FATAL = 'FATAL'

    class App(models.TextChoices):
        REPACKING = 'Prebaľovanie'
        USER_MANAGMENT = 'Správa používateľov'
        MAIL_REPORTS = 'Posielanie mailov'
        LOGGING = 'logovanie'

    text = models.CharField("Text", max_length=500, default="")
    action_time = models.DateTimeField("Čas", auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             related_name='user', verbose_name="Používateľ")
    priority = models.CharField(max_length=10, choices=Priority.choices, verbose_name="Priorita")
    app = models.CharField(max_length=25, choices=App.choices, verbose_name="Modul")

    @staticmethod
    def make_log(app, priority, user, text):
        Log(app=app, priority=priority, user=user, text=text).save()

    @staticmethod
    def filter_and_order_logs_by_get(get):
        order_by = get.get('order_by', "-action_time")
        try:
            if order_by in ('user__username', '-user__username'):
                pass
            elif order_by[0] == '-':
                Log._meta.get_field(order_by[1:])
            else:
                Log._meta.get_field(order_by)
        except:
            order_by = "action_time"
        logs = Log.objects.filter(
            text__contains=get.get('text', ""),
            priority__contains=get.get('priority', ""),
            app__contains=get.get('app', ""),
            #user__username__contains=get.get('username', ""),
        ).order_by(order_by)
        return logs

    def __str__(self):
        return f"Log {str(self.id)}"
