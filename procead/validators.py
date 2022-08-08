from datetime import date

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_positive(value):
    if value <= 0:
        raise ValidationError(
            _('Favor utilizar um valor inteiro maior que 0'),
            params={'value': value},
        )

def validate_is_zero_or_positive(value):
    if value < 0:
        raise ValidationError(
            _('Favor utilizar um valor inteiro maior ou igual a 0'),
            params={'value': value},
        )
        
def validate_national_phone_number(value):
    if len(value) <= 13:
        raise ValidationError(
            _('Favor adicionar um telefone no formato DDD + 8 dígitos ou DDD + 9 dígitos')
        )
        
def validate_edital_year(value):
    if value < 2012 or value > date.today().year + 1:
        raise ValidationError(
            _('O ano do edital não é válido.')
        )