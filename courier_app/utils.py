import calendar
import os
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.validators import RegexValidator

from django.utils.translation import gettext as _
from datetime import datetime

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,9}$', message="El núm. de celular no es válido, el formato válido es: 999999999")

ruc_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$', message="El núm. de ruc no es válido, deben ser 10 números")

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path=result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path
    

def get_date_now():
    now = datetime.now()
    day_name = _(calendar.day_name[0])
    month_name = _(calendar.month_name[3])

    date_now = "{}, {} de {}".format(day_name, now.day, month_name)
    
    return date_now

def get_title_now(request):
    if request.user.is_client:
        title = 'Resumen de hoy'
    else:
        title = 'Ganancias de hoy'
    return title

    