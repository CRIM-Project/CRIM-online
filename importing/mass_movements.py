import csv
import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crim.settings')
import django

django.setup()

from collections import OrderedDict

from crim.models.genre import CRIMGenre
from crim.models.piece import CRIMPiece

FILE_IN = 'source/CRIM_Mass_Catalog.csv'
FILE_OUT = '../crim/fixtures/mass_movements.json'


def process_roles(csvfile):
    '''Takes a csv file, rearranges the data as appropriate
    for the CRIM Django site, and exports the data as an
    OrderedDict.'''
    data = []
    csvreader = csv.DictReader(csvfile)
    for old_row in csvreader:
        pdf_links = old_row['PDF links'].split('|')
        mei_links = old_row['MEI links'].split('|')
        # For each of the five mass movements, create the piece
        # and add the correct links.
        for i in range(5):
            new_fields = OrderedDict()
            new_fields['piece_id'] = old_row['CRIM_Mass_ID'] + '_' + str(i+1)
            movement_titles = dict((y, x) for x, y in CRIMPiece.MASS_MOVEMENT_ORDER)
            new_fields['title'] = movement_titles[str(i+1)]
            new_fields['genre'] = CRIMGenre.objects.get(name='Mass').genre_id
            new_fields['pdf_links'] = pdf_links[i]
            new_fields['mei_links'] = mei_links[i]
            new_fields['mass'] = old_row['CRIM_Mass_ID']

            new_mass_movement_row = {
                'model': 'crim.crimpiece',
                'fields': new_fields,
            }

            data.append(new_mass_movement_row)
    return data


if __name__ == '__main__':
    with open(FILE_IN, encoding='utf-8', newline='') as csvfile:
        data = process_roles(csvfile)
    with open(FILE_OUT, 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(data))
