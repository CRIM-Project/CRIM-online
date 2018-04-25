from django.template.defaultfilters import register

from crim.common import get_date_sort


@register.filter(name='shortendate')
def shortendate(text):
    date_sort = get_date_sort(text)
    if '?' in text:
        return str(date_sort) + '?'
    elif 'c.' in text:
        return 'c. ' + str(date_sort)
    else:
        return str(date_sort)
