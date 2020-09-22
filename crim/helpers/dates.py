import re

from crim.helpers.common import get_nonempty

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

def get_date_sort(date):
    '''Given a date, return an integer year that approximates
    the latest date in the list.
    If given a string instead of a list, perform the evaluation
    on just the one string.
    '''
    if not date:
        return None

    yyyy_mm_dd = r'.*([0-9x]{4})-[0-9x]{2}-[0-9x]{2}[^0-9]*'
    yyyy = r'.*([0-9x]{4})[^0-9]*'
    yyy = r'.*([0-9x]{3})[^0-9]*'
    if re.match(yyyy_mm_dd, date):
        match = re.match(yyyy_mm_dd, date)
    elif re.match(yyyy, date):
        match = re.match(yyyy, date)
    else:
        match = re.match(yyy, date)
    return int(match.group(1).replace('x', '0')) if match else None

def earliest_date(dates):
    '''Takes a list of dates as strings, parses them,
    and returns the earliest one.'''
    if not dates:
        return None
    else:
        return get_nonempty(dates[0], latest_date(dates[1:]), min, get_date_sort)

def latest_date(dates):
    '''Takes a list of dates as strings, parses them,
    and returns the latest one.'''
    if not dates:
        return None
    else:
        return get_nonempty(dates[0], latest_date(dates[1:]), max, get_date_sort)
