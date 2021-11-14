from django.db import models


class Log(models.Model):
    text = models.CharField(max_length=500, default="")
    action_time = models.DateTimeField(auto_now=True)
