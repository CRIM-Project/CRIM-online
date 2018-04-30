import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crim.settings')
import django

from crim.import.analysis_constants import *

django.setup()

FILE_IN = 'source/citations.json'
FILE_OUT = '../crim/fixtures/analysis.json'


def create_entry_for_item(scores, assertions, relationships, creation, user, new_data):
    new_observations = []
    for observation in new_observations:
        observation['observation_id'] = TODO
        observation['observer'] = TODO
        observation['piece'] = TODO
        observation['ema'] = TODO
        observation['remarks'] = TODO
        observation['created'] = TODO
        observation['updated'] = TODO
        observation['needs_review'] = TODO


def process_json(old_data):
    new_data = []
    for item in old_data:
        create_entry_for_item(
            new_data,
            item['scores'],
            item['assertions'],
            item['relationships'],
            item['created_at'],
            item['user'],
        )
        if 'assertions' in item and item['assertions']:
            for assertion in item['assertions']:
                if 'ema' not in assertion and assertion['type']:
                    pass  # print(assertion)
        for relationship in item['relationships']:
            if 'scoreA_ema' not in relationship and 'scoreB_ema' not in relationship:
                if eval(item['user']) in USERS_TO_KEEP:
                    print(item['relationships'])
    return new_data


if __name__ == '__main__':
    with open(FILE_IN, encoding='utf-8', newline='') as oldjsonfile:
        datastore = json.load(oldjsonfile)
        new_data = process_json(datastore)
    with open(FILE_OUT, 'w', encoding='utf-8') as newjsonfile:
        newjsonfile.write(json.dumps(new_data))
