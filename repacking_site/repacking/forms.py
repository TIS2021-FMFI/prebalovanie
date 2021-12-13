from django import forms


class RepackingStandardForm(forms.Form):
    SKU = forms.CharField(max_length=50, required=True, label='SKU')
    COFOR = forms.CharField(max_length=50, required=True, label='COFOR')
    supplier = forms.CharField(max_length=50, required=True, label='Supplier')
    destination = forms.CharField(max_length=50, required=True, label='Destination')
    items_per_move = forms.IntegerField(required=True, label='Items per move')
    unit_weight = forms.DecimalField(max_digits=6, decimal_places=4, required=True, label='Unit weight')
    repacking_duration = forms.IntegerField(required=True, label='Repacking duration')
    instructions = forms.CharField(max_length=1200, required=True, label='Instructions')

    input_count_of_items_in_package = forms.IntegerField(required=True, label='Input count of items in package')
    output_count_of_items_in_package = forms.IntegerField(required=True, label='Output count of items in package')

    input_count_of_boxes_on_pallet = forms.IntegerField(required=True, label='Input count of boxes on pallet')
    output_count_of_boxes_on_pallet = forms.IntegerField(required=True, label='Output count of boxes on pallet')

    input_count_of_items_on_pallet = forms.IntegerField(required=True, label='Input count of items on pallet')
    output_count_of_items_on_pallet = forms.IntegerField(required=True, label='Output count of items on pallet')

    input_type_of_package = forms.CharField(max_length=50, required=True, label='Input type of package')
    output_type_of_package = forms.CharField(max_length=50, required=True, label='Output type of package')

    input_photos = forms.ImageField(label='Input photos', required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    output_photos = forms.ImageField(label='Output photos', required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))

    tools = forms.ImageField(label='Tools', required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))


class RepackingForm(forms.Form):
    SKU = forms.CharField(max_length=50, required=True)
    IDP = forms.CharField(max_length=50, required=True)
    operator_1 = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'id': 'id_operator-1'}))
