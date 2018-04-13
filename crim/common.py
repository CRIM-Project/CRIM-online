from dateutil.parser import parse


def get_date_sort(dates):
    '''Given a list of dates, return an integer year that approximates
    the latest date in the list.'''
    parsed_dates = []
    for date in dates:
        try:
            parsed_dates.append(parse(date.replace('x', '0').replace('?', ''), fuzzy=True).year)
        except ValueError:
            parsed_dates.append(0)
    return max(parsed_dates)
