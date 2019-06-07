import csv
import json

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crim.settings')
# import django

# from importing.analysis_constants import *

# django.setup()

CSV_FILE = 'source/batch1/batch1.csv'
FILE_OUT = 'source/batch1/batch1-untouched.json'


def convert_to_json():
    '''Given an input nested JSON file from Omeka, create a cleaned JSON
    file that is simpler in structure.
    '''
    extracted_data = []
    with open(CSV_FILE, encoding='utf-8', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            this_row_formatted = '{' + row['text'] + '}'
            this_row_json = json.loads(this_row_formatted)
            extracted_data.append(this_row_formatted)
    with open(FILE_OUT, 'w', encoding='utf-8') as outfile:
        outfile.write(json.dumps(extracted_data, indent=2))


if __name__ == '__main__':
    convert_to_json()
