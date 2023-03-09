from django import template
from django.utils.safestring import mark_safe

register  = template.Library()

UP_ARROW = '&#9650;'
DN_ARROW = '&#9660;'

@register.simple_tag(takes_context=True)
def sortable_header(context, title, param, value, default = False):
    request = context['request']
    qparam = request.GET.get(param, '')
    if (default and qparam == '') or (qparam == value):
        title, value = f'{title} {UP_ARROW}', f'-{value}'
    elif qparam == f'-{value}':
        title = f'{title} {DN_ARROW}'
    return mark_safe(f'<a href="?{param}={value}">{title}</a>')
