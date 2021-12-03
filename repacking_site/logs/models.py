from django.db import models
from django.conf import settings


class Log(models.Model):

    class Priority(models.TextChoices):
        TRACE = 'TRACE'
        DEBUG = 'DEBUG'
        INFO = 'INFO'
        WARNING = 'WARNING'
        ERROR = 'ERROR'
        FATAL = 'FATAL'

    class App(models.TextChoices):
        REPACKING = 'REPACKING'
        USER_MANAGMENT = 'USER_MANAGMENT'
        MAIL_REPORTS = 'MAIL_REPORTS'
        LOGGING = 'LOGGING'

    text = models.CharField(max_length=500, default="")
    action_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='user')
    priority = models.CharField(max_length=10, choices=Priority.choices)
    app = models.CharField(max_length=15, choices=App.choices)

    @staticmethod
    def make_log(app, priority, user, text):
        Log(app=app, priority=priority, user=user, text=text).save()

    @staticmethod
    def filter_and_order_logs_by_get(get):
        order_by = get.get('order_by', "action_time")
        try:
            if order_by[0] == '-':
                Log._meta.get_field(order_by[1:])
            else:
                Log._meta.get_field(order_by)
        except:
            order_by = "action_time"
        logs = Log.objects.filter(
            text__contains=get.get('text', ""),
            priority__contains=get.get('priority', ""),
            app__contains=get.get('app', ""),
        ).order_by(order_by)
        return logs

    def __str__(self):
        return str(self.app) + ", " + str(self.priority) + ", " + str(self.text) + ", " + str(self.action_time)
