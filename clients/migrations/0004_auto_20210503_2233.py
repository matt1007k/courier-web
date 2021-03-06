# Generated by Django 3.1.7 on 2021-05-04 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_client_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='clients/', verbose_name='logo de la tienda (opcional)'),
        ),
        migrations.AlterField(
            model_name='client',
            name='store_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre de tienda (opcional)'),
        ),
    ]
