from drivers.models import Driver
from .models import DriverPayment

def payment_to_drivers():
    drivers = Driver.objects.all()

