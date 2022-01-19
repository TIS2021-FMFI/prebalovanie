import django_filters
from django.forms import DateInput, DateTimeInput
from django_filters import DateFilter, DateTimeFilter
from django_filters import CharFilter

from .models import *


class LogFilter(django_filters.FilterSet):
    start_date = DateTimeFilter(field_name='action_time', lookup_expr='gte', label="Vytvorené od",
                                widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    end_date = DateTimeFilter(field_name='action_time', lookup_expr='lte', label="Vytvorené do",
                              widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    text = CharFilter(field_name='text', lookup_expr='icontains', label="Informácie")

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
