from django.template.defaultfilters import register


@register.filter(name='figuredash')
def figuredash(s):
    return str(s).replace('-', '–')
