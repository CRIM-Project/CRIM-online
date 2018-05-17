from django.template.defaultfilters import register


@register.filter(name='newlineplural')
def newlineplural(s):
    '''Check the string for newlines, indicating a list with
    more than one item. If a newline is found, return 's' which
    allows the label to be plural; otherwise, return the
    empty string.'''
    return 's' if '\n' in s else ''
