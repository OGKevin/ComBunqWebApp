# from captcha.fields import CaptchaField
from django import forms
# from .validator import checkUsername


class GenerateKeyForm(forms.Form):
    """docstring for GenerateKeyForm.
    Represents the form shown on /generate"""
    API = forms.CharField(label='API key', widget=forms.Textarea)
    encryption_password = forms.CharField(
        widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        password = self.cleaned_data.get('encryption_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data


class decrypt_form(forms.Form):
    """docstring for decrypt_form.
    Represents the form shown on /decrypt
    This form can be replaced with a form directly on HTML
    """
    encrypted_file = forms.FileField()
    encryption_password = forms.CharField(widget=forms.PasswordInput)
