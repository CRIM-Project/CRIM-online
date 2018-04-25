import csv
import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crim.settings')
import django

django.setup()

from collections import OrderedDict

from crim.common import get_date_sort
from crim.models.person import CRIMPerson

FILE_IN = 'source/CRIM_Mass_Catalog.csv'
FILE_OUT = '../crim/fixtures/mass_roles.json'


def add_composer(old_row, new_role_fields):
    new_role_fields['person'] = old_row['Composer']
    new_role_fields['role_type'] = 'composer'
    new_role_fields['mass'] = old_row['CRIM_Mass_ID']
    new_role_fields['date'] = old_row['Date of Mass']
    new_role_fields['date_sort'] = get_date_sort(old_row['Date of Mass'])


def add_editor(old_row, new_role_fields):
    new_role_fields['person'] = CRIMPerson.objects.get(name=old_row['Editor']).person_id
    new_role_fields['role_type'] = 'editor'
    new_role_fields['date'] = old_row['Date']
    new_role_fields['date_sort'] = get_date_sort(old_row['Date'])
    new_role_fields['mass'] = old_row['CRIM_Mass_ID']


def process_roles(csvfile):
    '''Takes a csv file, rearranges the data as appropriate
    for the CRIM Django site, and exports the data as an
    OrderedDict.'''
    data = []
    csvreader = csv.DictReader(csvfile)
    for old_row in csvreader:
        new_composer_fields = OrderedDict()
        new_editor_fields = OrderedDict()

        add_composer(old_row, new_composer_fields)
        add_editor(old_row, new_editor_fields)

        new_composer_row = {
            'model': 'crim.crimrole',
            'fields': new_composer_fields,
        }
        new_editor_row = {
            'model': 'crim.crimrole',
            'fields': new_editor_fields,
        }

        data.append(new_composer_row)
        data.append(new_editor_row)
    return data


if __name__ == '__main__':
    with open(FILE_IN, encoding='utf-8', newline='') as csvfile:
        data = process_roles(csvfile)
    with open(FILE_OUT, 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(data))
