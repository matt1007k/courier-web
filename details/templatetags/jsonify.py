from django import template
from django.utils.safestring import mark_safe
from django.core.serializers import serialize
import json

register = template.Library()

@register.filter()
def jsonify(list):
    qs = serialize('json', [list])
    # return mark_safe(json.dumps(list))
    return mark_safe(qs)