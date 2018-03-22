from django.template.defaultfilters import register


@register.filter(name='apostrophe')
def apostrophe(s):
    return str(s).replace("'", "’")
