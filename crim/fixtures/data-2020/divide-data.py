import json

# This script is for separating a dumped crimdata file into fixtures
# that can be imported without dependencies.


MODELS = {
    'crim.crimgenre': '1',
    'crim.crimmass': '2',
    'crim.crimpiece': '3',
    'sites.site': '4',
    'flatpages.flatpage': '5',
    'admin.logentry': 'skip',
}

LAST = 'last'

big_fixture = json.loads(open('crimdata.json', 'r').read())

new_fixtures = {LAST: []}
for model in MODELS.items():
    new_fixtures[model[1]] = []

for item in big_fixture:
    model = item.get('model')
    if model not in MODELS:
        new_fixtures[LAST].append(item)
    else:
        new_fixtures[MODELS[model]].append(item)

for fixture in new_fixtures.items():
    with open('crimdata/' + fixture[0] + '.json', 'w') as file:
        file.write(json.dumps(fixture[1]))
