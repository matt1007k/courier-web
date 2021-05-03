# Generated by Django 3.1.7 on 2021-05-02 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignDeliveryAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'asignar dirección de envío',
                'verbose_name_plural': 'direcciones de envío asignadas',
            },
        ),
        migrations.CreateModel(
            name='AssignOriginAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'asignar dirección de entrega',
                'verbose_name_plural': 'direcciones de entrega asignadas',
            },
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('SM', 'Pequeño'), ('MD', 'Mediano'), ('LG', 'Grande')], default='SM', max_length=100, verbose_name='tamaño')),
                ('contain', models.CharField(max_length=100, verbose_name='¿Qué contiene?')),
                ('value', models.CharField(max_length=150, verbose_name='valor del paquete')),
                ('image', models.ImageField(blank=True, null=True, upload_to='details-order/%Y/%m/%d/', verbose_name='imagen del paquete')),
                ('description', models.TextField(blank=True, max_length=200, null=True, verbose_name='nota')),
                ('distance', models.DecimalField(decimal_places=1, default=0, max_digits=10, verbose_name='distancia')),
                ('price_rate', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Precio de tarifa')),
                ('status', models.CharField(choices=[('PE', 'Pendiente'), ('RE', 'Recibido'), ('AL', 'En Almacén'), ('ER', 'En Ruta'), ('EN', 'Entregado'), ('NEN', 'No Entregado'), ('REPR', 'Reprogramado')], default='PE', max_length=50)),
                ('address_destiny', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address_destiny', to='addresses.address', verbose_name='dirección de destino')),
                ('address_origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address_origin', to='addresses.address', verbose_name='dirección de recojo')),
            ],
            options={
                'verbose_name': 'detalle',
                'verbose_name_plural': 'detalles',
            },
        ),
        migrations.CreateModel(
            name='UnassignOriginAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='details.detail', verbose_name='detalles del packete')),
            ],
            options={
                'verbose_name': 'sin asignar dirección de recojo',
                'verbose_name_plural': 'direcciones de recojo sin asignar',
            },
        ),
        migrations.CreateModel(
            name='UnassignDeliveryAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='details.detail', verbose_name='detalles del packete')),
            ],
            options={
                'verbose_name': 'sin asignar dirección de envío',
                'verbose_name_plural': 'direcciones de envío sin asignar ',
            },
        ),
        migrations.CreateModel(
            name='PackageDelivered',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='orders/delivered/%Y/%m/%d/', verbose_name='imagen o foto 1')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='orders/delivered/%Y/%m/%d/', verbose_name='imagen o foto 2')),
                ('description', models.TextField(blank=True, max_length=250, null=True, verbose_name='nota (opcional)')),
                ('detail', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='details.detail', verbose_name='dirección de envío')),
            ],
            options={
                'verbose_name': 'entrega de dirección de envío',
                'verbose_name_plural': 'entrega de direcciones de envío',
            },
        ),
    ]
