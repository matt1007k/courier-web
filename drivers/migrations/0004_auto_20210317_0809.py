# Generated by Django 3.1.7 on 2021-03-17 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0003_driver_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='cell_phone2',
            field=models.CharField(blank=True, max_length=9, null=True, verbose_name='Num. de celular 2'),
        ),
    ]
