from django import forms
from django.forms import ModelForm
from .models import RepackingStandard


class StandardUpdateForm(ModelForm):
    class Meta:
        model = RepackingStandard
        fields = ['SKU',
                  'COFOR',
                  'supplier',
                  'destination',
                  'items_per_move',
                  'unit_weight',
                  'repacking_duration',
                  'instructions',
                  'tools',
                  'input_count_of_items_in_package',
                  'output_count_of_items_in_package',
                  'input_count_of_boxes_on_pallet',
                  'output_count_of_boxes_on_pallet',
                  'input_count_of_items_on_pallet',
                  'output_count_of_items_on_pallet',
                  'input_type_of_package',
                  'output_type_of_package',
                  'input_photos',
                  'output_photos']

    def __init__(self, *args, **kwargs):
        super(StandardUpdateForm, self).__init__(*args, **kwargs)
        self.fields['SKU'].label = "SKU"
        self.fields['COFOR'].label = "COFOR"
        self.fields['supplier'].label = "Dodávateľ"
        self.fields['destination'].label = "Destinácia"
        self.fields['input_photos'].label = "Foto IN"
        self.fields['output_photos'].label = "Foto OUT"
        self.fields['tools'].label = "Ochranné pomôcky"
        self.fields['items_per_move'].label = "Počet kusov na jeden pohyb"
        self.fields['input_type_of_package'].label = "Typ obalu IN"
        self.fields['output_type_of_package'].label = "Typ obalu OUT"
        self.fields['unit_weight'].label = "Jednotková váha dielu"
        self.fields['input_count_of_items_in_package'].label = "Počet ks v balení IN"
        self.fields['output_count_of_items_in_package'].label = "Počet ks v balení OUT"
        self.fields['input_count_of_boxes_on_pallet'].label = "Počet boxov na palete IN"
        self.fields['output_count_of_boxes_on_pallet'].label = "Počet boxov na palete OUT"
        self.fields['input_count_of_items_on_pallet'].label = "Počet kusov na palete IN"
        self.fields['output_count_of_items_on_pallet'].label = "Počet kusov na palete OUT"
        self.fields['unit_weight'].label = "Jednotková váha dielu"
        self.fields['repacking_duration'].label = "Čas prebalu"
        self.fields['instructions'].label = "Poznámka"


class RepackingStandardForm(forms.Form):
    SKU = forms.CharField(max_length=50, required=True, label='SKU')
    COFOR = forms.CharField(max_length=50, required=True, label='COFOR')
    supplier = forms.CharField(max_length=50, required=True, label='Dodávateľ')
    destination = forms.CharField(max_length=50, required=True, label='Miesto určenia')
    items_per_move = forms.IntegerField(required=True, label='Počet kusov na jeden pohyb')
    unit_weight = forms.DecimalField(max_digits=6, decimal_places=4, required=True, label='Jednotková váha dielu')
    repacking_duration = forms.IntegerField(required=True, label='Doba prebaľovania')
    instructions = forms.CharField(max_length=1200, required=True, label='Inštrukcie / pokyny')

    input_count_of_items_in_package = forms.IntegerField(required=True, label='Vstupný počet kusov v balení')
    output_count_of_items_in_package = forms.IntegerField(required=True, label='Výstupný počet kusov v balení')

    input_count_of_boxes_on_pallet = forms.IntegerField(required=True, label='Vstupný počet boxov na palete')
    output_count_of_boxes_on_pallet = forms.IntegerField(required=True, label='Výstupný počet boxov na palete')

    input_count_of_items_on_pallet = forms.IntegerField(required=True, label='Vstupný počet kusov na palete')
    output_count_of_items_on_pallet = forms.IntegerField(required=True, label='Výstupný počet kusov na palete')

    input_type_of_package = forms.CharField(max_length=50, required=True, label='Vstupný typ obalu')
    output_type_of_package = forms.CharField(max_length=50, required=True, label='Výstupný typ obalu')

    input_photos = forms.ImageField(label='Vstupné fotografie', required=False,
                                    widget=forms.ClearableFileInput(attrs={'multiple': True}))
    output_photos = forms.ImageField(label='Výstupné fotografie', required=False,
                                     widget=forms.ClearableFileInput(attrs={'multiple': True}))

    tools = forms.ImageField(label='Ochranné pomôcky', required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))


class RepackingForm(forms.Form):
    SKU = forms.CharField(max_length=50, required=True)
    IDP = forms.CharField(max_length=50, required=True)
    operator_1 = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'id': 'id_operator-1'}))
