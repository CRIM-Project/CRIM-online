#!/bin/bash

set -e

python manage.py makemigrations
python manage.py migrate

# python manage.py loaddata /app/duchemin/data/duchemin_dcperson.json
# python manage.py loaddata /app/duchemin/data/duchemin_dcbook.json
# python manage.py loaddata /app/duchemin/data/duchemin_dccontentblock.json
# python manage.py loaddata /app/duchemin/data/duchemin_dcpiece.json
# python manage.py loaddata /app/duchemin/data/duchemin_dcreconstruction.json
# python manage.py loaddata /app/duchemin/data/duchemin_dcphrase.json
# python manage.py loaddata /app/duchemin/data/duchemin_dcanalysis.json
# python manage.py loaddata /app/duchemin/data/duchemin_dcnote.json


python manage.py runserver 0.0.0.0:8000
