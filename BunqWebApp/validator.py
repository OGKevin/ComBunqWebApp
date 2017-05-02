from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


def checkUsername(userName):
    if User.objects.filter(username=userName).exists():
        raise ValidationError(
            _('%(value)s already exists'),
            params={'value': userName},
        )
