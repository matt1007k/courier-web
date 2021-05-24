from datetime import datetime

def get_generate_tracking_code():
    # details_count = Detail.objects.exclude(tracking_code=None).count()

    now = datetime.now()
    year = str(now.year)[-2:]
    month = now.month
    hour = add_zero_to_number(now.hour)
    minute = add_zero_to_number(now.minute)
    seg = add_zero_to_number(now.second)

    code_text = '{}{}{}{}'.format(year, month, minute, seg)

    return 'CC{}'.format(code_text)


def add_zero_to_number(min):
    if min < 10:
        return "0%s" % min

    return min