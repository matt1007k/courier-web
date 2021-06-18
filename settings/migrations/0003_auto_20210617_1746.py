# Generated by Django 3.1.7 on 2021-06-17 22:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_auto_20210617_1712'),
    ]

    operations = [
        migrations.RenameField(
            model_name='setting',
            old_name='time_limit',
            new_name='time_limit_from',
        ),
        migrations.AddField(
            model_name='setting',
            name='time_limit_to',
            field=models.TimeField(blank=True, default=datetime.time(8, 0), verbose_name='tiempo de abrir del sistema'),
        ),
    ]
