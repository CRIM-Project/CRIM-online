import re


def get_date_sort(date):
    '''Given a date, return an integer year that approximates
    the latest date in the list.

    If given a string instead of a list, perform the evaluation
    on just the one string.
    '''
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
    if dates:
        earliest_date = dates[0]
        for date in dates:
            if (get_date_sort(date) and get_date_sort(earliest_date) and
                    get_date_sort(date) and get_date_sort(date) < get_date_sort(earliest_date)):
                earliest_date = date
        return earliest_date
    else:
        return None


def latest_date(dates):
    '''Takes a list of dates as strings, parses them,
    and returns the latest one.'''
    if dates:
        latest_date = dates[0]
        for date in dates:
            if (get_date_sort(date) and get_date_sort(latest_date) and
                    get_date_sort(date) and get_date_sort(date) > get_date_sort(latest_date)):
                latest_date = date
        return latest_date
    else:
        return None
