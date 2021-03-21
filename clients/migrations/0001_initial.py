# Generated by Django 3.1.7 on 2021-03-19 18:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=150, verbose_name='Apellidos')),
                ('address', models.CharField(max_length=200, verbose_name='Dirección')),
                ('address_gps', models.JSONField(verbose_name='Dirección GPS')),
                ('logo', models.ImageField(upload_to='clients/')),
                ('store_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre de tienda')),
                ('driver_code', models.CharField(max_length=12, verbose_name='código de motorizado')),
                ('social_media', models.JSONField(blank=True, null=True, verbose_name='redes sociales')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
    ]
