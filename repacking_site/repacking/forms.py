from django import forms


class RepackingStandardForm(forms.Form):
    SKU_code = forms.CharField(max_length=50, required=False)
    COFOR_code = forms.CharField(max_length=50, required=False)
    supplier = forms.CharField(max_length=50, required=False)
    destination = forms.CharField(max_length=50, required=False)
    pcs_per_move = forms.IntegerField(required=False)
    unit_weight = forms.DecimalField(max_digits=6, decimal_places=4, required=False)
    repacking_time = forms.IntegerField(required=False)
    remark = forms.CharField(max_length=1200, required=False)

    pcs_package_in = forms.IntegerField(required=False)
    pcs_package_out = forms.IntegerField(required=False)

    boxes_on_pallet_in = forms.IntegerField(required=False)
    boxes_on_pallet_out = forms.IntegerField(required=False)

    pcs_on_pallet_in = forms.IntegerField(required=False)
    pcs_on_pallet_out = forms.IntegerField(required=False)

    package_type_in = forms.CharField(max_length=50, required=False)
    package_type_out = forms.CharField(max_length=50, required=False)
