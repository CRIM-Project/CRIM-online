import csv
import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crim.settings')
import django

django.setup()

from collections import OrderedDict
from crim.models.document import CRIMSource
from crim.models.mass import CRIMMass
from crim.models.piece import CRIMPiece

FILE_IN = 'source/CRIM_Source_Catalog.csv'
FILE_OUT = '../crim/fixtures/source.json'


def add_contents(contents, fields):
    mass_contents = []
    piece_contents = []
    for item in contents:
        if 'Model' in item:
            piece = CRIMPiece.objects.get(piece_id=item)
            piece_contents.append(piece.pk)
        elif 'Mass' in item:
            mass = CRIMMass.objects.get(mass_id=item)
            mass_contents.append(mass.pk)
        else:
            print('Can’t tell what type {} is'.format(item))
    if mass_contents:
        fields['mass_contents'] = mass_contents
    if piece_contents:
        fields['piece_contents'] = piece_contents


def add_source(old_row, new_fields):
    new_fields['document_id'] = old_row['CRIM_Source_ID']
    if old_row['Title']:
        new_fields['title'] = old_row['Title']
    else:
        new_fields['title'] = '[' + old_row['Copies Used (Location)'] + ']'
    if old_row['Ms'].lower() in (1, 'y', 'yes'):
        new_fields['source_type'] = CRIMSource.MANUSCRIPT
    else:
        new_fields['source_type'] = CRIMSource.PRINT
    contents = old_row['Contents'].split(' | ')
    add_contents(contents, new_fields)
    new_fields['remarks'] = 'Copy used: ' + old_row['Copies Used (Location)']
    new_fields['external_links'] = old_row['URL of Facsimile']


def process_source(csvfile):
    '''Takes a csv file, rearranges the data as appropriate
    for the CRIM Django site, and exports the data as an
    OrderedDict.'''
    data = []
    csvreader = csv.DictReader(csvfile)
    for old_row in csvreader:
        new_fields = OrderedDict()
        add_source(old_row, new_fields)

        new_source_row = {
            'model': 'crim.crimsource',
            'fields': new_fields,
        }
        data.append(new_source_row)
    return data


if __name__ == '__main__':
    with open(FILE_IN, encoding='utf-8', newline='') as csvfile:
        data = process_source(csvfile)
    with open(FILE_OUT, 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(data))
