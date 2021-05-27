from datetime import datetime
from random import randint

def get_generate_tracking_code():
    # details_count = Detail.objects.exclude(tracking_code=None).count()

    now = datetime.now()
    year = str(now.year)[-2:]
    month = add_zero_to_number(now.month)
    hour = add_zero_to_number(now.hour)
    minute = add_zero_to_number(now.minute)
    seg = add_zero_to_number(now.second)
    rand_interger = randint(0, 9)

    code_text = '{}{}{}{}'.format(year, month, minute, seg + rand_interger)

    return 'CC{}'.format(code_text)


def add_zero_to_number(min):
    if min < 10:
        return "0%s" % min

    return min