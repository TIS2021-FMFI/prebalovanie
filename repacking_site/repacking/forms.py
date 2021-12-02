from django import forms


class RepackingStandardForm(forms.Form):
    SKU = forms.CharField(max_length=50, required=True)
    COFOR = forms.CharField(max_length=50, required=True)
    supplier = forms.CharField(max_length=50, required=True)
    destination = forms.CharField(max_length=50, required=True)
    items_per_move = forms.IntegerField(required=True)
    unit_weight = forms.DecimalField(max_digits=6, decimal_places=4, required=True)
    repacking_duration = forms.IntegerField(required=True)
    instructions = forms.CharField(max_length=1200, required=True)

    input_count_of_items_in_package = forms.IntegerField(required=True)
    output_count_of_items_in_package = forms.IntegerField(required=True)

    input_count_of_boxes_on_pallet = forms.IntegerField(required=True)
    output_count_of_boxes_on_pallet = forms.IntegerField(required=True)

    input_count_of_items_on_pallet = forms.IntegerField(required=True)
    output_count_of_items_on_pallet = forms.IntegerField(required=True)

    input_type_of_package = forms.CharField(max_length=50, required=True)
    output_type_of_package = forms.CharField(max_length=50, required=True)

    input_photos = forms.ImageField(required=False)
    output_photos = forms.ImageField(required=False)

    tools = forms.ImageField(required=False)
