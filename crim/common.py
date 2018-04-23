import re


def get_date_sort(dates):
    '''Given a list of dates, return an integer year that approximates
    the latest date in the list.

    If given a string instead of a list, perform the evaluation
    on just the one string.
    '''
    if isinstance(dates, str):
        dates = [dates]
    parsed_dates = []
    yyyy_mm_dd = r'.*([0-9x]{4})-[0-9x]{2}-[0-9x]{2}[^0-9]*'
    yyyy = r'.*([0-9x]{4})[^0-9]*'
    for date in dates:
        match = re.match(yyyy, date) if re.match(yyyy, date) else re.match(yyyy_mm_dd, date)
        if match:
            date_int = int(match[1].replace('x', '0'))
            parsed_dates.append(date_int)
        else:
            parsed_dates.append(0)
    return max(parsed_dates)


def earliest_date(dates):
    if dates:
        earliest_date = dates[0]
        for date in dates:
            if get_date_sort(date) < get_date_sort(earliest_date):
                earliest_date = date
        return earliest_date
    else:
        return '-'
