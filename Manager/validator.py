from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import json
import requests


def ibanValidator(iban):
    '''
    checks if the provided iban is a valid one before storing it into the
    database.
    '''
    url = 'https://openiban.com/validate/'
    check = json.loads(requests.get(
        "".join([url, iban])).content.decode())
    if not check['valid']:
        raise ValidationError(
            _('%(value)s is not a valid IBAN number'),
            params={'value': iban},
        )
