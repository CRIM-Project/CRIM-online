import csv
import json
import os

from collections import OrderedDict
from crim.common import two_digit_string

PATH_IN = 'source/model_phrases'
FILE_IN_LIST = os.listdir(PATH_IN)
FILE_OUT = '../crim/fixtures/model_phrases.json'


def add_phrase(old_row, new_fields):
    part_with_default = old_row['Part'] if old_row['Part'] else '1'
    new_fields['phrase_id'] = old_row['CRIM_Model_ID'] + ':' + two_digit_string(old_row['Model_Phrase_Number'])
    new_fields['piece'] = old_row['CRIM_Model_ID']
    new_fields['part'] = old_row['CRIM_Model_ID'] + '.' + part_with_default
    new_fields['number'] = eval(old_row['Model_Phrase_Number'])
    new_fields['start_measure'] = eval(old_row['Start_Measure'])
    new_fields['stop_measure'] = eval(old_row['Stop_Measure'])
    new_fields['text'] = old_row['Text']
    new_fields['translation'] = old_row['Translation']


def add_part(old_row, new_fields, existing_parts):
    part_with_default = old_row['Part'] if old_row['Part'] else '1'
    part_id = old_row['CRIM_Model_ID'] + '.' + part_with_default
    if part_id in existing_parts:
        pass
    else:
        new_fields['part_id'] = part_id
        new_fields['piece'] = old_row['CRIM_Model_ID']
        new_fields['order'] = eval(part_with_default)
        existing_parts.append(part_id)


def process_phrase(csvfile):
    '''Takes a csv file, rearranges the data as appropriate
    for the CRIM Django site, and exports the data as an
    OrderedDict.'''
    this_phrase_data = []
    existing_parts = []  # list of part IDs, eg ('CRIM_Model_0001.1')
    csvreader = csv.DictReader(csvfile)

    for old_row in csvreader:
        # There are a whole bunch of empty rows that shouldn't be added
        if old_row['Start_Measure']:
            new_part_fields = OrderedDict()
            add_part(old_row, new_part_fields, existing_parts)
            # Check to make sure we're not adding duplicate parts
            if new_part_fields:
                new_part_row = {
                    'model': 'crim.crimpart',
                    'fields': new_part_fields,
                }
                this_phrase_data.append(new_part_row)

            new_phrase_fields = OrderedDict()
            add_phrase(old_row, new_phrase_fields)
            new_phrase_row = {
                'model': 'crim.crimphrase',
                'fields': new_phrase_fields,
            }
            data.append(new_phrase_row)
    return this_phrase_data


if __name__ == '__main__':
    data = []
    for filename in FILE_IN_LIST:
        if filename.endswith('.csv'):
            with open(os.path.join(PATH_IN, filename), encoding='utf-8', newline='') as csvfile:
                data += process_phrase(csvfile)
    with open(FILE_OUT, 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(data))
