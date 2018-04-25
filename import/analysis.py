import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crim.settings')
import django
from pprint import pprint

django.setup()

FILE_IN = 'source/citations.json'
FILE_OUT = '../crim/fixtures/analysis.json'

pieces = {
    'Sohier. Missa Vidi speciosam (Kyrie)': 'CRIM_Mass_0002_1',
    'Sohier. Missa Vidi speciosam (Gloria)': 'CRIM_Mass_0002_2',
    'Sohier. Missa Vidi speciosam (Credo)': 'CRIM_Mass_0002_3',
    'Sohier. Missa Vidi speciosam (Sanctus)': 'CRIM_Mass_0002_4',
    'Sohier. Missa Vidi speciosam (Agnus)': 'CRIM_Mass_0002_5',
    'Marle. Missa O gente brunette (Kyrie)': 'CRIM_Mass_0003_1',
    'Marle. Missa O gente brunette (Gloria)': 'CRIM_Mass_0003_2',
    'Marle. Missa O gente brunette (Credo)': 'CRIM_Mass_0003_3',
    'Marle. Missa O gente brunette (Sanctus)': 'CRIM_Mass_0003_4',
    'Marle. Missa O gente brunette (Agnus)': 'CRIM_Mass_0003_5',
    'Clereau. Missa Virginis Mariae (Kyrie)': 'CRIM_Mass_0004_1',
    'Févin. Missa Ave Maria (Kyrie)': 'CRIM_Mass_0005_1',
    'Guyon. Missa Je suis déshéritée (Kyrie)': 'CRIM_Mass_0006_1',
    'Gombert. Missa Je suis déshéritée (Kyrie)': 'CRIM_Mass_0007_1',
    'Gombert. Missa Je suis déshéritée (Gloria)': 'CRIM_Mass_0007_2',
    'Sermisy. Missa Quare fremuerunt gentes (Kyrie)': 'CRIM_Mass_0008_1',
    'Sermisy. Missa Quare fremuerunt gentes (Gloria)': 'CRIM_Mass_0008_2',
    'Sermisy, Claudin de: Sermisy. Missa Tota pulchra es (Kyrie)': 'CRIM_Mass_0009_1',
    'Sermisy, Claudin de: Sermisy. Missa Tota pulchra es (Gloria)': 'CRIM_Mass_0009_2',
    'Sermisy, Claudin de: Sermisy. Missa Tota pulchra es (Credo)': 'CRIM_Mass_0009_3',
    'Sermisy, Claudin de: Sermisy. Missa Tota pulchra es (Sanctus)': 'CRIM_Mass_0009_4',
    'Sermisy, Claudin de: Sermisy. Missa Tota pulchra es (Agnus)': 'CRIM_Mass_0009_5',
    'Févin. Missa Mente tota (Kyrie)': 'CRIM_Mass_0014_1',
    'Févin. Missa Mente tota (Gloria)': 'CRIM_Mass_0014_2',
    'Palestrina. Missa Benedicta es (Kyrie)': 'CRIM_Mass_0015_1',
    'Palestrina. Missa Benedicta es (Gloria)': 'CRIM_Mass_0015_2',
    'Palestrina. Missa Benedicta es (Credo)': 'CRIM_Mass_0015_3',
    'Palestrina. Missa Benedicta es (Sanctus)': 'CRIM_Mass_0015_4',
    'Palestrina. Missa Benedicta es (Agnus)': 'CRIM_Mass_0015_5',
    'Forestier, Mathurin: Forestier. Missa Baisés moy ma doulce amye (Kyrie)': 'CRIM_Mass_0017_1',
    'Forestier, Mathurin: Forestier. Missa Baisés moy ma doulce amye (Gloria)': 'CRIM_Mass_0017_2',
    'Forestier, Mathurin: Forestier. Missa Baisés moy ma doulce amye (Credo)': 'CRIM_Mass_0017_3',
    'Forestier, Mathurin: Forestier. Missa Baisés moy ma doulce amye (Sanctus)': 'CRIM_Mass_0017_4',
    'Forestier, Mathurin: Forestier. Missa Baisés moy ma doulce amye (Agnus)': 'CRIM_Mass_0017_5',
    'Palestrina. Missa Veni sponsa Christi (Kyrie)': 'CRIM_Mass_0019_1',
    'Palestrina. Missa Veni sponsa Christi (Gloria)': 'CRIM_Mass_0019_2',
    'Palestrina. Missa Veni sponsa Christi (Credo)': 'CRIM_Mass_0019_3',
    'Palestrina. Missa Veni sponsa Christi (Sanctus)': 'CRIM_Mass_0019_4',
    'Palestrina. Missa Veni sponsa Christi (Agnus)': 'CRIM_Mass_0019_5',
    'Lassus, Roland de: Lassus. Missa Susanne un jour (Kyrie)': 'CRIM_Mass_0020_1',
    'Lassus, Roland de: Lassus. Missa Susanne un jour (Gloria)': 'CRIM_Mass_0020_2',
    'Lassus, Roland de: Lassus. Missa Susanne un jour (Credo)': 'CRIM_Mass_0020_3',
    'Lassus, Roland de: Lassus. Missa Susanne un jour (Sanctus)': 'CRIM_Mass_0020_4',
    'Lassus, Roland de: Lassus. Missa Susanne un jour (Agnus)': 'CRIM_Mass_0020_5',
    'Lupi. Vidi speciosam sicut columbam': 'CRIM_Model_0001',
    'Champion. O gente brunette': 'CRIM_Model_0002',
    'Anonymus. Graduale triplex - Kyrie': 'CRIM_Model_0003',
    'Josquin. Ave Maria': 'CRIM_Model_0008',
    'Cadéac. Je suis déshéritée': 'CRIM_Model_0009',
    'Sermisy. Quare fremuerunt gentes': 'CRIM_Model_0010',
    'Sermisy, Claudin de: Sermisy. Tota pulchra es': 'CRIM_Model_0011',
    'Josquin. Mente Tota': 'CRIM_Model_0016',
    'Josquin. Benedicta es': 'CRIM_Model_0017',
    'Josquin Des Prés: Josquin. Baises moy': 'CRIM_Model_0018',
    'Palestrina. Veni sponsa Christi': 'CRIM_Model_0019',
    'Lassus, Roland de: Lassus. Susanne un jour': 'CRIM_Model_0020',
    'Benedicta es,cælorum Regina': 'CRIM_Model_0021',
    'Benedicta es': 'CRIM_Model_0022',
    'Lupi, Didier: Lupi. Susanne un jour': 'CRIM_Model_0024',
}


def process_json(old_data):
    new_data = []
    all_pieces = []
    ids_with_voices = []
    for item in old_data:
        relationships = item['relationships']
        assertions = item['assertions']
        scores = item['scores']
        creation = item['created_at']
        user = item['user']
    return new_data


if __name__ == '__main__':
    with open(FILE_IN, encoding='utf-8', newline='') as oldjsonfile:
        datastore = json.load(oldjsonfile)
        new_data = process_json(datastore)
    with open(FILE_OUT, 'w', encoding='utf-8') as newjsonfile:
        newjsonfile.write(json.dumps(new_data))
