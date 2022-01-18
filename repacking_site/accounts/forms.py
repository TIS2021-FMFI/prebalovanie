from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from django.forms import ModelForm


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True, label="Krstné meno")
    last_name = forms.CharField(max_length=50, required=True, label="Priezvisko")
    barcode = forms.CharField(max_length=50, required=True, label="Čiarový kód")


class NewUserForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True, label="Krstné meno")
    last_name = forms.CharField(max_length=50, required=True, label="Priezvisko")
    user_name = forms.CharField(max_length=50, required=True, label="Používateľské meno")
    password = forms.CharField(widget=forms.PasswordInput, label="Heslo")
    barcode = forms.CharField(max_length=50, required=True, label="Čiarový kód")


class NewGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions', ]


