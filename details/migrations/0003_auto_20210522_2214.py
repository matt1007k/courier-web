# Generated by Django 3.1.7 on 2021-05-23 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0002_auto_20210504_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='status',
            field=models.CharField(choices=[('PE', 'Pendiente'), ('RE', 'Recibido'), ('AL', 'En Almacén'), ('ER', 'En Ruta'), ('EN', 'Entregado'), ('NEN', 'No Entregado'), ('REPR', 'Reprogramado')], default='PE', max_length=50, verbose_name='estado'),
        ),
    ]
