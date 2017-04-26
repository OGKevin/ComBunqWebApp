from captcha.fields import CaptchaField
from django import forms


class GenerateKeyForm(forms.Form):
    """docstring for GenerateKeyForm."""
    captcha = CaptchaField()
    password = forms.CharField(label='password', min_length=8)
    # API = forms.CharField(label='API')
