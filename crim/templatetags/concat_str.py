from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def concat_str(value_1, value_2):
    return str(value_1).lower().replace(" ", "-") + "-" + str(value_2).lower().replace(" ", "-")