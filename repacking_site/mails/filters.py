import django_filters
from django_filters import CharFilter

from .models import *

class EmailListFilter(django_filters.FilterSet):
    mail = CharFilter(field_name='mail', lookup_expr='icontains', label='Email')

    class Meta:
        model = MailSendSetting
        fields = ['mail']
