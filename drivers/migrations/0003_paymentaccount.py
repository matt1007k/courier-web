# Generated by Django 3.1.7 on 2021-04-19 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0002_auto_20210324_1648'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(max_length=150, verbose_name='banco')),
                ('account_number', models.CharField(max_length=14, verbose_name='número de cuenta')),
                ('bank_account_number', models.CharField(max_length=20, verbose_name='número de cuenta interbancaria')),
                ('owners', models.CharField(max_length=150, verbose_name='nombre completo del titular')),
                ('dni', models.CharField(max_length=8, verbose_name='DNI del titular')),
                ('driver', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='drivers.driver', verbose_name='motorizado')),
            ],
            options={
                'verbose_name': 'cuenta de pago',
                'verbose_name_plural': 'cuentas de pago',
            },
        ),
    ]