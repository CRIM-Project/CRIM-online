import csv
import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crim.settings')
import django

django.setup()

from collections import OrderedDict

from crim.common import get_date_sort

FILE_IN = 'source/CRIM_Source_Catalog.csv'
FILE_OUT = '../crim/fixtures/source_roles.json'

ANONYMOUS = 'CRIM_Person_0012'


def add_publisher(old_row, new_role_fields, publisher_id=ANONYMOUS):
    new_role_fields['person'] = publisher_id
    new_role_fields['role_type'] = 'publisher'
    new_role_fields['date'] = old_row['Date']
    new_role_fields['date_sort'] = get_date_sort(old_row['Date'])
    new_role_fields['source'] = old_row['CRIM_Source_ID']


def process_roles(csvfile):
    '''Takes a csv file, rearranges the data as appropriate
    for the CRIM Django site, and exports the data as an
    OrderedDict.'''
    data = []
    csvreader = csv.DictReader(csvfile)
    for old_row in csvreader:
        publishers = old_row['Person_ID of Publisher'].split(' | ')
        # If there are listed publishers, add one role per publisher listed
        if old_row['Person_ID of Publisher']:
            for publisher_id in publishers:
                new_publisher_fields = OrderedDict()
                add_publisher(old_row, new_publisher_fields, publisher_id)
                new_publisher_row = {
                    'model': 'crim.crimrole',
                    'fields': new_publisher_fields,
                }
                data.append(new_publisher_row)
        # Otherwise, add publisher as "anonymous" if only to add the date
        else:
            new_publisher_fields = OrderedDict()
            add_publisher(old_row, new_publisher_fields, publisher_id=ANONYMOUS)
            new_publisher_row = {
                'model': 'crim.crimrole',
                'fields': new_publisher_fields,
            }
            data.append(new_publisher_row)
    return data


if __name__ == '__main__':
    with open(FILE_IN, encoding='utf-8', newline='') as csvfile:
        data = process_roles(csvfile)
    with open(FILE_OUT, 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(data))
