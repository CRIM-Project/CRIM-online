from django.template.defaultfilters import register


@register.filter(name='newline_to_break_tag')
def newline_to_break_tag(s):
    return str(s).replace('\n', '; ')
