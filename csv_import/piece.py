import csv
import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crim.settings')
import django

django.setup()
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crim.settings')

from collections import OrderedDict
from crim.models.genre import CRIMGenre
# from itertools import count

FILE_IN = 'source/CRIM_Model_Catalog.csv'
FILE_OUT = '../crim/fixtures/piece.json'


def add_piece(old_row, new_fields):
    new_fields['piece_id'] = old_row['CRIM_Model_ID']
    new_fields['title'] = old_row['Title']
    new_fields['genre'] = CRIMGenre.objects.get(name=old_row['Genre of Model']).genre_id
    new_fields['remarks'] = old_row['Notes']
    new_fields['mei_links'] = old_row['MEI link'].replace(' | ', '\n')
    new_fields['pdf_links'] = old_row['PDF link'].replace(' | ', '\n')


def process_piece(csvfile):
    '''Takes a csv file, rearranges the data as appropriate
    for the CRIM Django site, and exports the data as an
    OrderedDict.'''
    data = []
    csvreader = csv.DictReader(csvfile)
    for old_row in csvreader:
        new_fields = OrderedDict()
        add_piece(old_row, new_fields)

        new_piece_row = {
            'model': 'crim.crimpiece',
            'fields': new_fields,
        }
        data.append(new_piece_row)
    return data


if __name__ == '__main__':
    with open(FILE_IN, encoding='utf-8', newline='') as csvfile:
        data = process_piece(csvfile)
    with open(FILE_OUT, 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(data))
