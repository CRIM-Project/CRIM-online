import json
import os

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crim.settings')
# import django

# from importing.analysis_constants import *

# django.setup()

FILE_IN = 'source/batch3/complete-citations.json'
FILE_OUT = 'source/batch3/complete-peeled.json'


def simplify():
    '''Given an input nested JSON file from Omeka, create a cleaned JSON
    file that is simpler in structure.
    '''
    extracted_data = []
    with open(FILE_IN, encoding='utf-8', newline='') as raw_json_file:
        nested_data = json.load(raw_json_file)
    for item in nested_data:
        item_text = item['text']
        item_data = json.loads(item_text)
        extracted_data.append(item_data)
    with open(FILE_OUT, 'w', encoding='utf-8') as simplified_file:
        simplified_file.write(json.dumps(extracted_data, indent=2))


if __name__ == '__main__':
    simplify()
