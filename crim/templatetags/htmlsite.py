from django.template.defaultfilters import register


@register.filter(name='htmlsite')
def htmlsite(url):
    '''Removes `data/` from a URL so that the human-readable site
    is shown.'''
    return url.replace('/data/', '/')
