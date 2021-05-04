# Generated by Django 3.1.7 on 2021-05-04 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0004_driver_created_at'),
        ('details', '0003_auto_20210503_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagedelivered',
            name='driver',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='drivers.driver', verbose_name='motorizado'),
        ),
    ]
