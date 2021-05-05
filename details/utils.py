from .models import Detail

def get_generate_tracking_code():
    details_count = Detail.objects.exclude(tracking_code=None).count()
    # if details_count <= 1:
    #     details_count = 0

    zero = ''
    
    if details_count < 10:
        zero = '00000'
    if details_count >= 10:
        zero = '0000'
    if details_count >= 100:
        zero = '000'
    if details_count >= 1000:
        zero = '00'
    if details_count >= 10000:
        zero = '0'
    if details_count >= 100000:
        zero = ''

    code = '{}{}'.format(zero, details_count + 1)
    return 'CC{}'.format(code)