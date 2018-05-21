from django.template.defaultfilters import register


@register.filter(name='firstitem')
def firstitem(items, delimiter='\n'):
    '''Returns only the first item in a list.'''
    if isinstance(items, str):
        l = items.split(delimiter)
        return l[0] if l else ''
    else:
        return items[0]
