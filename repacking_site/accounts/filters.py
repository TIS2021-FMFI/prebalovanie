import django_filters
from django_filters import CharFilter

from .models import *


class UserFilter(django_filters.FilterSet):
    first_name = CharFilter(field_name='first_name', lookup_expr='icontains', label="Krstné meno")
    last_name = CharFilter(field_name='last_name', lookup_expr='icontains', label="Priezvisko")
    barcode = CharFilter(field_name='barcode', lookup_expr='icontains', label="Barcode")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'barcode']

    # navod na premenovanie labelov: https://stackoverflow.com/questions/31686157/django-set-filter-field-label-or-verbose-name
    # alebo treba pozriet napr. logs/filters na inspiraciu...
