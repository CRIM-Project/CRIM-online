import re

OMAS = 'https://ema.crimproject.org/'

def two_digit_string(n):
    '''Converts a number into an equivalent string;
    prefixes a 0 if the number has only one digit.
    '''
    # We expect an integer, but will convert strings.
    if isinstance(n, str):
        n = eval(n)

    if n >= 0 and n < 10:
        return '0' + str(n)
    else:
        return str(n)

def get_nonempty(a, b, comparator, processor):
    '''Return the higher of function(a) and function(b),
    with None counting as lowest.'''
    if processor(a) is None:
        return b
    elif processor(b) is None:
        return a
    else:
        return comparator(a, b)

def cache_values_to_string(id, page_number):
    if page_number is None:
        return str(id) + ','
    else:
        return str(id) + ',' + str(page_number)
