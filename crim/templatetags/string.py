from django.template.defaultfilters import register


@register.filter(name='string')
def string(i):
    return str(i)
