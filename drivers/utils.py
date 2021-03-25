from .models import Driver

def generate_driver_code():
    drivers_count = Driver.objects.count()
    generate_number = drivers_count + 1
    zero = ''
    
    if drivers_count < 10:
        zero = '000'
    if drivers_count >= 10:
        zero = '00'
    if drivers_count >= 100:
        zero = '0'
    if drivers_count >= 1000:
        zero = ''

    code = '{}{}'.format(zero, generate_number)
    return 'CLICK{}'.format(code)