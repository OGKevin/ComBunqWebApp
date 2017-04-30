# from captcha.fields import CaptchaField
from django import forms
# from .validator import checkUsername


class GenerateKeyForm(forms.Form):
    """docstring for GenerateKeyForm."""
    # captcha = CaptchaField()
    username = forms.CharField(
        label='username', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    API = forms.CharField(label='API key', widget=forms.Textarea)
    encryption_password = forms.CharField(widget=forms.PasswordInput)
