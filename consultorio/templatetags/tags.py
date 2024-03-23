from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter
def multiply_and_format(value, arg):
    """
    Custom filter to multiply the given value by the argument and add a thousands separator.
    """
    try:
        result = int(value) * int(arg)
        return intcomma(result)
    except (ValueError, TypeError):
        return value


@register.filter
def traducir(value):
    """
    Traduce el valor
    """
    return value.replace('hour', 'hora').replace('minute', 'minuto').replace('segundo', 'segundos')
