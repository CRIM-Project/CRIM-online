import csv
import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crim.settings')
import django

django.setup()

from collections import OrderedDict
from crim.models.genre import CRIMGenre

FILE_IN = 'source/CRIM_Mass_Catalog.csv'
FILE_OUT = '../crim/fixtures/mass.json'


def add_mass(old_row, new_fields):
    new_fields['mass_id'] = old_row['CRIM_Mass_ID']
    new_fields['title'] = old_row['Title']
    new_fields['genre'] = CRIMGenre.objects.get(name='Mass').genre_id
    new_fields['remarks'] = old_row['Notes']


def process_mass(csvfile):
    '''Takes a csv file, rearranges the data as appropriate
    for the CRIM Django site, and exports the data as an
    OrderedDict.'''
    data = []
    csvreader = csv.DictReader(csvfile)
    for old_row in csvreader:
        new_fields = OrderedDict()
        add_mass(old_row, new_fields)

        new_mass_row = {
            'model': 'crim.crimmass',
            'fields': new_fields,
        }
        data.append(new_mass_row)
    return data


if __name__ == '__main__':
    with open(FILE_IN, encoding='utf-8', newline='') as csvfile:
        data = process_mass(csvfile)
    with open(FILE_OUT, 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(data))
