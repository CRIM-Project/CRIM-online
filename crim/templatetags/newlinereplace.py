from django.template.defaultfilters import register


@register.filter(name='newlinereplace')
def newlinereplace(s, new_string='<br/>'):
    return str(s).replace('\n', new_string)
