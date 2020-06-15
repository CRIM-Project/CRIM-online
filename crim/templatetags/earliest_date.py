from django.template.defaultfilters import register

import crim.helpers.dates as dates


@register.filter(name='earliest_date')
def earliest_date(roles, role_types=''):
    '''Returns the earliest date from a list of dates.'''
    all_dates = dates.date_list(roles, role_types)
    return dates.earliest_date(all_dates) if all_dates else ''
