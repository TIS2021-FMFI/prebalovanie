import django_filters

from .models import *


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'barcode']

    # navod na premenovanie labelov: https://stackoverflow.com/questions/31686157/django-set-filter-field-label-or-verbose-name
    # alebo treba pozriet napr. logs/filters na inspiraciu...
    def __init__(self, *args, **kwargs):
        super(UserFilter, self).__init__(*args, **kwargs)
