# Generated by Django 3.1.7 on 2021-03-17 19:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0005_auto_20210317_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='first_name',
            field=models.CharField(default='d', max_length=100, verbose_name='Nombre'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='driver',
            name='last_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100, verbose_name='Apellidos'),
            preserve_default=False,
        ),
    ]
