import decimal
from service_prices.models import DriverPaymentRate


def apply_payment_rate(total, count):
    new_total = 0

    for payment_rate in DriverPaymentRate.objects.all():
        if count >= payment_rate.min and (count <= payment_rate.max or count >= payment_rate.max):
            new_total = round(total * decimal.Decimal(payment_rate.percentage / 100), 2)
        
    return new_total