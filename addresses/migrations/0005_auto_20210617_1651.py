# Generated by Django 3.1.7 on 2021-06-17 21:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0004_auto_20210614_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(max_length=150, verbose_name='dirección'),
        ),
        migrations.AlterField(
            model_name='address',
            name='email',
            field=models.CharField(blank=True, max_length=150, null=True, validators=[django.core.validators.EmailValidator()], verbose_name='correo electrónico'),
        ),
    ]
