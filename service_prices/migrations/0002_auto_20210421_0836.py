# Generated by Django 3.1.7 on 2021-04-21 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_prices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceprice',
            name='max',
            field=models.IntegerField(verbose_name='máximo de KM'),
        ),
        migrations.AlterField(
            model_name='serviceprice',
            name='min',
            field=models.IntegerField(default=0, verbose_name='mínimo de kM'),
        ),
    ]
