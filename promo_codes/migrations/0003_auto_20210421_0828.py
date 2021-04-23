# Generated by Django 3.1.7 on 2021-04-21 13:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promo_codes', '0002_auto_20210412_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='discount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='porcentaje de descuento'),
        ),
    ]