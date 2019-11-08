import re


OMAS = 'https://ema.crimproject.org/'


def two_digit_string(n):
    # We expect an integer, but will convert strings.
    if isinstance(n, str):
        n = eval(n)

    if n >= 0 and n < 10:
        return '0' + str(n)
    else:
        return str(n)


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


def get_nonempty(a, b, comparator, processor):
    '''Return the higher of function(a) and function(b),
    with None counting as lowest.'''
    if processor(a) is None:
        return b
    elif processor(b) is None:
        return a
    else:
        return comparator(a, b)


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


def cache_values_to_string(id, page_number):
    if page_number is None:
        return str(id) + ','
    else:
        return str(id) + ',' + str(page_number)
