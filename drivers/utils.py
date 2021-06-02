from random import randint

def generate_driver_code():
    code = randint(0, 9999)

    return 'CLICK{}'.format(code)