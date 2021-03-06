# Generated by Django 3.1.7 on 2021-05-24 16:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_auto_20210523_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='cell_phone',
            field=models.CharField(blank=True, max_length=9, null=True, validators=[django.core.validators.RegexValidator(message='El núm. de celular no es válido, el formato válido es: 999999999', regex='^\\+?1?\\d{9,9}$')], verbose_name='Núm. de celular'),
        ),
    ]
