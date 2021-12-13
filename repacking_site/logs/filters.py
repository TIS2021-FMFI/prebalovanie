import django_filters
from django_filters import DateFilter

from .models import *


class LogFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='action_time', lookup_expr='gte', label="Vytvorené od")
    end_date = DateFilter(field_name='action_time', lookup_expr='lte', label="Vytvorené do")

    class Meta:
        model = Log
        fields = ['app',
                  'priority',
                  'user',
                  'text']

    def __init__(self, *args, **kwargs):
        super(LogFilter, self).__init__(*args, **kwargs)
        self.filters['app'].label = "Typ"
        self.filters['priority'].label = "Úroveň"
        self.filters['user'].label = "Používateľ"
        self.filters['text'].label = "Informácie"