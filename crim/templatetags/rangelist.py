from django.template.defaultfilters import register
from math import ceil


@register.filter(name='rangelist')
def rangelist(i, pagesize):
    return range(1, ceil(i/pagesize)+1)
