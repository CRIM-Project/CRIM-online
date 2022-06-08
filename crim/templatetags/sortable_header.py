from django import template
from django.utils.safestring import mark_safe

register  = template.Library()

@register.simple_tag(takes_context=True)
def sortable_header(context, title, param, value, default = False):
    request = context['request']
    qparam = request.GET.get(param, '')
    output = f'<th><a href="?{param}={value}">{title}</a></th>'
    if (default and qparam == '') or (qparam == value):
        output = f'<th><a href="?{param}=-{value}">{title} &#9660;</a></th>'
    elif qparam == f'-{value}':
        output = f'<th><a href="?{param}={value}">{title} &#9650;</a></th>'
    return mark_safe(output)

