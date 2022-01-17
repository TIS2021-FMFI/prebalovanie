from django import forms


class ExportUpdateForm(forms.Form):
    date = forms.DurationField(label='Time of update (days)', required=True)


class AddEmailForm(forms.Form):
    email = forms.EmailField(required=True)
