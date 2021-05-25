from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,9}$', message="El núm. de celular no es válido, el formato válido es: 999999999")

ruc_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$', message="El núm. de ruc no es válido, deben ser 10 números")

    