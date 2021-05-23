from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_number(value):
    if type(value) is int:
        raise ValidationError(
            _('%(value)s no es un número'),
            params={'value': value}
        )