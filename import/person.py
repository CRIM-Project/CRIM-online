import csv
import json
import re
from collections import OrderedDict
from crim.common import get_date_sort

FILE_IN = 'source/CRIM_Person_Catalog.csv'
FILE_OUT = '../crim/fixtures/person.json'


def split_surname(s):
    '''Takes a surname given in a string, where the unsorted
    particle (eg 'de') is given in parentheses after the sorted
    part of the surname.
       Returns a tuple with the sorted part of the surname in the
    first element and the rest in the second. If there is no
    particle, the second element is empty.

    >>> split_surname('Du Chemin')
    ('Du Chemin', '')

    >>> split_surname('Palestrina (da)')
    ('Palestrina', 'da')
    '''
    pattern = r'([^(]*) \(([^)]*)\)'
    m = re.match(pattern, s)
    if m:
        return (m[1], m[2])
    else:
        return (s, '')


def add_person_id(old_row, new_fields):
    '''Use the information in `old_row`, an OrderedDict, to
    add the `person_id` field to `new_fields`.
    '''
    new_fields['person_id'] = old_row['CRIM_Person_ID']


def add_name(old_row, new_fields):
    firstname = old_row['Name']
    particle = split_surname(old_row['Surname'])[1]
    lastname = split_surname(old_row['Surname'])[0]
    alternates = old_row['Alternate Name'].replace('; ', '\n')

    if lastname and firstname:
        if particle:
            new_fields['name'] = firstname + ' ' + particle + ' ' + lastname
            new_fields['name_sort'] = lastname + ', ' + firstname + ' ' + particle
        else:
            new_fields['name'] = firstname + ' ' + lastname
            new_fields['name_sort'] = lastname + ', ' + firstname
    else:
        name = lastname if lastname else firstname
        new_fields['name'] = name
        new_fields['name_sort'] = name
    new_fields['name_alternate_list'] = alternates


def add_dates(old_row, new_fields):
    new_fields['birth_date'] = old_row['Birth Date']
    new_fields['death_date'] = old_row['Death Date']
    new_fields['active_date'] = old_row['Active Dates']

    all_dates = [old_row['Birth Date'],
                 old_row['Death Date'],
                 old_row['Active Dates']]

    if get_date_sort(all_dates) == 0:
        new_fields['date_sort'] = None
    else:
        new_fields['date_sort'] = get_date_sort(all_dates)


def process_person(csvfile):
    '''Takes a csv file, rearranges the data as appropriate
    for the CRIM Django site, and exports the data as an
    OrderedDict.'''
    data = []
    csvreader = csv.DictReader(csvfile)
    for old_row in csvreader:
        new_fields = OrderedDict()
        add_person_id(old_row, new_fields)
        add_name(old_row, new_fields)
        add_dates(old_row, new_fields)
        new_fields['remarks'] = ''

        new_row = {'model': 'crim.crimperson',
                   'fields': new_fields,
                   }
        data.append(new_row)
    return data


if __name__ == '__main__':
    with open(FILE_IN, encoding='utf-8', newline='') as csvfile:
        data = process_person(csvfile)
    with open(FILE_OUT, 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(data))
