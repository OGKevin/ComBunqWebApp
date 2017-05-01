from django import forms
from . import validator


class registration(forms.Form):
    """docstring for registration."""
    username = forms.CharField(
        max_length=150, validators=[validator.checkUsername])
    password = forms.CharField(
        widget=forms.PasswordInput, min_length=8
        )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords dont match')
        return self.cleaned_data
