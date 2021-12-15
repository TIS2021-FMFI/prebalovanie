import django_filters
from django_filters import CharFilter

from .models import *


class RepackingStandardFilter(django_filters.FilterSet):
    SKU = CharFilter(field_name='SKU', lookup_expr='icontains')
    COFOR = CharFilter(field_name='COFOR', lookup_expr='icontains')
    destination = CharFilter(field_name='destination', lookup_expr='icontains')

    class Meta:
        model = RepackingStandard
        fields = ['SKU',
                  'COFOR',
                  'destination',
                  'input_type_of_package',
                  'output_type_of_package']

    def __init__(self, *args, **kwargs):
        super(RepackingStandardFilter, self).__init__(*args, **kwargs)
        self.filters['destination'].label = "Destinácia"
        self.filters['input_type_of_package'].label = "Obal IN"
        self.filters['output_type_of_package'].label = "Obal OUT"


class RepackHistoryFilter(django_filters.FilterSet):
    repacking_standard__SKU = CharFilter(field_name='repacking_standard__SKU', lookup_expr='icontains')
    repacking_standard__COFOR = CharFilter(field_name='repacking_standard__COFOR', lookup_expr='icontains')
    repacking_standard__destination = CharFilter(field_name='repacking_standard__destination', lookup_expr='icontains')

    class Meta:
        model = RepackHistory
        fields = ['repacking_standard__SKU',
                  'repacking_standard__COFOR',
                  'repacking_standard__destination',
                  'repacking_standard__output_type_of_package',
                  'repacking_standard__output_count_of_items_in_package',
                  'repacking_standard__output_count_of_boxes_on_pallet',
                  'repacking_standard__output_count_of_items_on_pallet',
                  'repacking_standard__unit_weight',
                  'repacking_standard__supplier',
                  'repacking_standard__repacking_duration',
                  'repack_start',
                  'repack_finish',
                  'repack_duration',
                  'users']

    def __init__(self, *args, **kwargs):
        super(RepackHistoryFilter, self).__init__(*args, **kwargs)
        self.filters['repacking_standard__SKU'].label = "SKU"
        self.filters['repacking_standard__COFOR'].label = "COFOR"
        self.filters['repacking_standard__destination'].label = "Destinácia"
        self.filters['repacking_standard__output_type_of_package'].label = "Typ obalu OUT"
        self.filters['repacking_standard__output_count_of_items_in_package'].label = "Počet ks v balení OUT"
        self.filters['repacking_standard__output_count_of_boxes_on_pallet'].label = "Počet boxov na palete OUT"
        self.filters['repacking_standard__output_count_of_items_on_pallet'].label = "Počet kusov na palete OUT"
        self.filters['repacking_standard__unit_weight'].label = "Jednotková váha dielu"
        self.filters['repacking_standard__supplier'].label = "Dodávateľ"
        self.filters['repacking_standard__repacking_duration'].label = "Čas prebalu"
        self.filters['repack_start'].label = "Začiatok prebalu"
        self.filters['repack_finish'].label = "Koniec prebalu"
        self.filters['repack_duration'].label = "Celkový čas prebalu"
        self.filters['users'].label = "Operátori"
