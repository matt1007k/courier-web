import datetime
from random import randint

def get_generate_tracking_code():
    # details_count = Detail.objects.exclude(tracking_code=None).count()

    now = datetime.datetime.now()
    year = str(now.year)[-2:]
    month = add_zero_to_number(now.month)
    hour = add_zero_to_number(now.hour)
    minute = add_zero_to_number(now.minute)
    seg = add_zero_to_number(now.second)
    rand_integer = randint(1, 9)
    seg_random = str(seg + rand_integer)

    code_text = '{}{}{}{}'.format(year, month, minute, seg_random)

    return 'CC{}'.format(code_text)


def add_zero_to_number(min):
    if min < 10:
        return "0%s" % min

    return min

def get_time_now():
    now = datetime.datetime.now()
    hour = 0 if now.hour == 23 else now.hour
    time = datetime.time(hour, now.minute, now.second)
    return time