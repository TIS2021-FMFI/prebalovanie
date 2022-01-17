from django.contrib import admin

from .models import *


class LogsAdmin(admin.ModelAdmin):
    list_display = (str, 'priority', 'app', 'user', 'action_time', 'text')


admin.site.register(Log, LogsAdmin)
