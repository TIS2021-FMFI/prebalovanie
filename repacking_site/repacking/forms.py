from django import forms


class RepackingStandardForm(forms.Form):
    SKU = forms.CharField(max_length=50, required=False)
    COFOR = forms.CharField(max_length=50, required=False)
    supplier = forms.CharField(max_length=50, required=False)
    destination = forms.CharField(max_length=50, required=False)
    items_per_move = forms.IntegerField(required=False)
    unit_weight = forms.DecimalField(max_digits=6, decimal_places=4, required=False)
    repacking_duration = forms.IntegerField(required=False)
    instructions = forms.CharField(max_length=1200, required=False)

    input_count_of_items_in_package = forms.IntegerField(required=False)
    output_count_of_items_in_package = forms.IntegerField(required=False)

    input_count_of_boxes_on_pallet = forms.IntegerField(required=False)
    output_count_of_boxes_on_pallet = forms.IntegerField(required=False)

    input_count_of_items_on_pallet = forms.IntegerField(required=False)
    output_count_of_items_on_pallet = forms.IntegerField(required=False)

    input_type_of_package = forms.CharField(max_length=50, required=False)
    output_type_of_package = forms.CharField(max_length=50, required=False)
