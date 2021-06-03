from random import randint

def generate_driver_code():
    code = randint(1000, 9999)

    return 'CLICK{}'.format(code)