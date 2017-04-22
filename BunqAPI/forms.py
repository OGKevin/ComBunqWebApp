from captcha.fields import CaptchaField
from django import forms


class GenerateKeyForm(forms.Form):
    """docstring for GenerateKeyForm."""
    captcha = CaptchaField()
