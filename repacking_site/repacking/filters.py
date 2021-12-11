import django_filters

from .models import *


class RepackingStandardFilter(django_filters.FilterSet):
    class Meta:
        model = RepackingStandard
        fields = ['SKU',
                  'COFOR',
                  'destination',
                  'input_type_of_package',
                  'output_type_of_package']
