from django.template.defaultfilters import register


@register.filter(name='firstitem')
def firstitem(s, delimiter='\n'):
    '''Returns only the first item in a list.'''
    l = s.split(delimiter)
    return l[0] if l else ''
