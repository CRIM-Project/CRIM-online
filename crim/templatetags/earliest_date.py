from django.template.defaultfilters import register

import crim


def date_list(roles, role_types=''):
    '''Returns a list of dates given a list of roles. If role types
    are given, return only dates in roles with an acceptable role type.'''
    if not roles:
        return []
    else:
        # If no role type list has been given, allow all of them;
        # otherwise, restrict to those given.
        if roles[0]['role_type']['role_type_id'] in role_types.split(',') or not role_types:
            dates_to_add = [roles[0]['date']]
        else:
            dates_to_add = []
        return dates_to_add + date_list(roles[1:], role_types)


@register.filter(name='earliest_date')
def earliest_date(roles, role_types=''):
    '''Returns the earliest date from a list of dates.'''
    dates = date_list(roles, role_types)
    return crim.common.earliest_date(dates) if dates else ''
