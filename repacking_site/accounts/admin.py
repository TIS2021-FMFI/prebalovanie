from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission

from .models import User


class CustomUserCreationForm(UserCreationForm):
    barcode = forms.CharField(label='Barcode')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('barcode',)


class CustomUserChangeForm(UserChangeForm):
    barcode = forms.CharField(label='Barcode')

    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('barcode',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('barcode',)}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Permission)