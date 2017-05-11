# from captcha.fields import CaptchaField
from django import forms
# from .validator import checkUsername


class GenerateKeyForm(forms.Form):
    """docstring for GenerateKeyForm.
    Represents the form shown on /generate"""
    API = forms.CharField(label='API key', widget=forms.Textarea)
    encryption_password = forms.CharField(widget=forms.PasswordInput)


class decrypt_form(forms.Form):
    """docstring for decrypt_form.
    Represents the form shown on /decrypt
    This form can be replaced with a form directly on HTML
    """
    encrypted_file = forms.FileField()
    encryption_password = forms.CharField(widget=forms.PasswordInput)
