import django_filters
from django import forms
from django.forms import DateTimeInput, DateInput, TimeInput
from django_filters import CharFilter, DateTimeFilter, DurationFilter
from django_filters.widgets import RangeWidget
from durationwidget.widgets import TimeDurationWidget

from .models import *


class RepackingStandardFilter(django_filters.FilterSet):
    SKU = CharFilter(field_name='SKU', lookup_expr='icontains', label="SKU")
    COFOR = CharFilter(field_name='COFOR', lookup_expr='icontains', label="COFOR")
    destination = CharFilter(field_name='destination', lookup_expr='icontains', label="Destinácia")
    input_type_of_package = CharFilter(field_name='input_type_of_package', lookup_expr='icontains', label="Obal IN")
    output_type_of_package = CharFilter(field_name='output_type_of_package', lookup_expr='icontains', label="Obal OUT")

    class Meta:
        model = RepackingStandard
        fields = ['SKU',
                  'COFOR',
                  'destination',
                  'input_type_of_package',
                  'output_type_of_package']


class SplitDurationWidget(forms.MultiWidget):
    """
    A Widget that splits duration input into four number input boxes.
    """

    def __init__(self, attrs=None):
        widgets = (forms.NumberInput(attrs=attrs),
                   forms.NumberInput(attrs=attrs),
                   forms.NumberInput(attrs=attrs),
                   forms.NumberInput(attrs=attrs))
        super(SplitDurationWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            d = value
            if d:
                hours = d.seconds // 3600
                minutes = (d.seconds % 3600) // 60
                seconds = d.seconds % 60
                return [int(d.days), int(hours), int(minutes), int(seconds)]
        return [0, 1, 0, 0]


class RepackHistoryFilter(django_filters.FilterSet):
    repacking_standard__SKU = CharFilter(field_name='repacking_standard__SKU', lookup_expr='icontains', label="SKU")
    repacking_standard__COFOR = CharFilter(field_name='repacking_standard__COFOR',
                                           lookup_expr='icontains', label="COFOR")
    repacking_standard__destination = CharFilter(field_name='repacking_standard__destination',
                                                 lookup_expr='icontains', label="Destinácia")
    repacking_standard__output_type_of_package = CharFilter(field_name='repacking_standard__output_type_of_package',
                                                            lookup_expr='icontains', label="Typ obalu OUT")
    repacking_standard__input_type_of_package = CharFilter(field_name='repacking_standard__input_type_of_package',
                                                           lookup_expr='icontains', label="Typ obalu IN")
    repacking_standard__supplier = CharFilter(field_name='repacking_standard__supplier',
                                              lookup_expr='icontains', label="Dodávateľ")
    repack_start = DateTimeFilter(field_name='repack_start', lookup_expr='gte', label="Začiatok prebalu",
                                  widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    repack_finish = DateTimeFilter(field_name='repack_start', lookup_expr='lte', label="Koniec prebalu",
                                   widget=DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = RepackHistory
        fields = ['repacking_standard__SKU',
                  'repacking_standard__COFOR',
                  'repacking_standard__destination',
                  'repacking_standard__output_type_of_package',
                  'repacking_standard__input_type_of_package',
                  'repacking_standard__output_count_of_items_in_package',
                  'repacking_standard__output_count_of_boxes_on_pallet',
                  'repacking_standard__output_count_of_items_on_pallet',
                  'repacking_standard__unit_weight',
                  'repacking_standard__supplier',
                  'repacking_standard__repacking_duration',
                  'repack_duration',
                  'users']

    def __init__(self, *args, **kwargs):
        super(RepackHistoryFilter, self).__init__(*args, **kwargs)
        self.filters['repacking_standard__output_count_of_items_in_package'].label = "Počet ks v balení OUT"
        self.filters['repacking_standard__output_count_of_boxes_on_pallet'].label = "Počet boxov na palete OUT"
        self.filters['repacking_standard__output_count_of_items_on_pallet'].label = "Počet kusov na palete OUT"
        self.filters['repacking_standard__unit_weight'].label = "Jednotková váha dielu"
        self.filters['repacking_standard__repacking_duration'].label = "Čas prebalu"

        self.filters['repack_duration'].label = "Celkový čas prebalu"
        self.filters['users'].label = "Operátori"
