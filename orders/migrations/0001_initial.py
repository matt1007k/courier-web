# Generated by Django 3.1.7 on 2021-03-24 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_code', models.CharField(max_length=8, unique=True, verbose_name='Código de seguimiento')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROCESS', 'In Process'), ('DELIVERED', 'Delivered'), ('CANCELED', 'Canceled')], default='PENDING', max_length=50, verbose_name='Estado')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('type_ticket', models.CharField(choices=[('FACTURA', 'Factura'), ('BOLETA', 'Boleta')], default='FACTURA', max_length=10, verbose_name='Comprobante electrónico')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.client', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'pedido',
                'verbose_name_plural': 'pedidos',
            },
        ),
    ]
