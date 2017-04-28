# from captcha.fields import CaptchaField
from django import forms
# from .validator import checkUsername


class GenerateKeyForm(forms.Form):
    """docstring for GenerateKeyForm."""
    # captcha = CaptchaField()
    password = forms.CharField(widget=forms.PasswordInput)
    # API = forms.CharField(label='API')
    userID = forms.CharField(
        label='userID', max_length=150)
