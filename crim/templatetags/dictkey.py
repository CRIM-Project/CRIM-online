from django.template.defaultfilters import register


@register.filter(name='dictkey')
def dictkey(d, k):
    '''Returns the given key from a dictionary.'''
    return d.get(k)
