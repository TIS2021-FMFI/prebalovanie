from django import forms


class EmailTimeForm(forms.Form):
    time = forms.TimeField(label='Čas posielania mailov', required=True)


class AddEmailForm(forms.Form):
    email = forms.EmailField(required=True)
