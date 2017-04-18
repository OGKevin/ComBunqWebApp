from django.core.exceptions import ValidationError
import json
import requests
from django.utils.translation import ugettext_lazy as _


def ibanValidator(iban):
    url = 'https://openiban.com/validate/'
    check = json.loads(requests.get(
        "".join([url, iban])).content.decode())
    if check['valid']:
        print ('valid IBAN number')
    else:
        raise ValidationError(
            _('%(value)s is not a valid IBAN number'),
            params={'value': iban},
        )
