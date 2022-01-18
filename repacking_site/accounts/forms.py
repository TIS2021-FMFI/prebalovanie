from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from django.forms import ModelForm


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True, label="Krstné meno")
    last_name = forms.CharField(max_length=50, required=True, label="Priezvisko")
    barcode = forms.CharField(max_length=50, required=True, label="Čiarový kód")


class NewUserForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'first_name', 'last_name', 'email',
                  'barcode', 'groups', 'is_superuser', 'is_staff', 'is_active']
        help_texts = {
            'username': None,
            'groups': None,
            'is_superuser': None,
            'is_staff': None,
            'is_active': None,
        }

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.fields['password'].label = "Heslo"
        self.fields['is_superuser'].label = "Superadmin:"
        self.fields['username'].label = "Používateľské meno"
        self.fields['username'].widget = forms.TextInput(attrs={'autofocus': True})
        self.fields['first_name'].label = "Krstné meno"
        self.fields['last_name'].label = "Priezvisko"
        self.fields['email'].label = "Email"
        self.fields['is_staff'].label = "Má prístup do admin rozhrania"
        self.fields['is_active'].label = "Aktívny"
        self.fields['barcode'].label = "Čiarový kód"
        self.fields['groups'].label = "Skupiny"


class NewGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions', ]

    def __init__(self, *args, **kwargs):
        super(NewGroupForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Názov"
        self.fields['permissions'].label = "Práva"

        user_choices = []
        selected = []
        for user in get_user_model().objects.all():
            user_choices.append((user.id, user.username))
            if self.instance.pk is not None and user in self.instance.user_set.all():
                selected.append(user.id)

        self.fields['users'] = forms.MultipleChoiceField(choices=user_choices, label="Používatelia", initial=selected)
