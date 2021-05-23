from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,9}$', message="El núm. de celular no es válido, es formato válido es: 999999999")