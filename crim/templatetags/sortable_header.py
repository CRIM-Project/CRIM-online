from django import template
from django.utils.safestring import mark_safe

register  = template.Library()

@register.simple_tag(takes_context=True)
def sortable_header(context, title, param, value, default = False):
    request = context['request']
    qparam = request.GET.get(param, '')
    if (default and qparam == '') or (qparam == value):
        title, value = f'{title} &#9660;', f'-{value}'
    elif qparam == f'-{value}':
        title = f'{title} &#9650;'
    return mark_safe(f'<a href="?{param}={value}">{title}</a>')

