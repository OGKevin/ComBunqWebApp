# from captcha.fields import CaptchaField
from django import forms
# from .validator import checkUsername


class GenerateKeyForm(forms.Form):
    """docstring for GenerateKeyForm.
    Represents the form shown on /generate"""
    API = forms.CharField(label='API key', widget=forms.Textarea)
    user_password = forms.CharField(
        widget=forms.PasswordInput, min_length=8)


class MyBunqForm(forms.Form):
    """docstring for my_bunq_form.
    Represents the form shown on /my_bunq
    This form can be replaced with a form directly on HTML
    """
    encrypted_file = forms.FileField()
    encryption_password = forms.CharField(widget=forms.PasswordInput)
