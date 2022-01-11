from django.template.defaultfilters import register


@register.filter(name='capitalize')
def capitalize(s):
    return s.capitalize()
