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
    yyyy_mm_dd = r'.*([0-9][0-9][0-9][0-9])-[0-9][0-9]-[0-9][0-9][^0-9]*'
    yyyy = r'.*([0-9][0-9][0-9][0-9])[^0-9]*'
    for date in dates:
        if re.match(yyyy, date):
            parsed_dates.append(re.match(yyyy, date)[1])
        elif re.match(yyyy_mm_dd, date):
            parsed_dates.append(re.match(yyyy_mm_dd, date)[1])
        else:
            parsed_dates.append(0)
    return max(parsed_dates)
