# Generated by Django 3.1.7 on 2021-05-04 19:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        ('drivers', '0004_driver_created_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('details', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='pedido'),
        ),
        migrations.AddField(
            model_name='assignoriginaddress',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='administrador'),
        ),
        migrations.AddField(
            model_name='assignoriginaddress',
            name='detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='details.detail', verbose_name='detalles del paquete'),
        ),
        migrations.AddField(
            model_name='assignoriginaddress',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drivers.driver', verbose_name='motorizado'),
        ),
        migrations.AddField(
            model_name='assigndeliveryaddress',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='administrador'),
        ),
        migrations.AddField(
            model_name='assigndeliveryaddress',
            name='detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='details.detail', verbose_name='detalles del paquete'),
        ),
        migrations.AddField(
            model_name='assigndeliveryaddress',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drivers.driver', verbose_name='motorizado'),
        ),
    ]
