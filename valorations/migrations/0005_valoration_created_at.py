# Generated by Django 3.1.7 on 2021-04-11 03:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('valorations', '0004_auto_20210410_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='valoration',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='fecha de creación'),
            preserve_default=False,
        ),
    ]