import csv
import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crim.settings')
import django

django.setup()

from collections import OrderedDict

FILE_IN = 'source/staffLabels.csv'
FILE_OUT = '../crim/fixtures/voices.json'

LINKS_TO_PIECE_ID = {
    'http://92.154.49.37/CRIM/files/original/055666e19ab020e13902378ef638c5f0.mei': 'CRIM_Mass_0001_1',
    'http://92.154.49.37/CRIM/files/original/da6d1ce377f97dbb1ab1c734c3025ba3.mei': 'CRIM_Mass_0001_2',
    'http://92.154.49.37/CRIM/files/original/711308080cd07562b4aeabab2663534b.mei': 'CRIM_Mass_0001_3',
    'http://92.154.49.37/CRIM/files/original/5813b93dac855c858e008c679cca350c.mei': 'CRIM_Mass_0001_4',
    'http://92.154.49.37/CRIM/files/original/23e1bf64f64c9de4fd074855970658f3.mei': 'CRIM_Mass_0001_5',
    'http://92.154.49.37/CRIM/files/original/7ed0710885b124a22e55c0b7c4e7177d.mei': 'CRIM_Mass_0002_1',
    'http://92.154.49.37/CRIM/files/original/ea2e4483952322bfae02245ef838ce84.mei': 'CRIM_Mass_0002_2',
    'http://92.154.49.37/CRIM/files/original/2839e783847fec9e1eb287850cc7806f.mei': 'CRIM_Mass_0002_3',
    'http://92.154.49.37/CRIM/files/original/076954e0cc129d16e521173ba8ed1702.mei': 'CRIM_Mass_0002_4',
    'http://92.154.49.37/CRIM/files/original/13bbb050e5dd5cd701b8db0946e58c87.mei': 'CRIM_Mass_0002_5',
    'http://92.154.49.37/CRIM/files/original/b685e0cf1de3ac7d9700ce97383c1753.mei': 'CRIM_Mass_0003_1',
    'http://92.154.49.37/CRIM/files/original/9a62bbe90b447f5b92e3f05a085cd1fb.mei': 'CRIM_Mass_0003_2',
    'http://92.154.49.37/CRIM/files/original/a06a32be97d3ca7da00869cb4329f54d.mei': 'CRIM_Mass_0003_3',
    'http://92.154.49.37/CRIM/files/original/e30222028979b52bddd4058742b3e273.mei': 'CRIM_Mass_0003_4',
    'http://92.154.49.37/CRIM/files/original/5bbea703ec9480f6f24dff7076d84f98.mei': 'CRIM_Mass_0003_5',
    'http://92.154.49.37/CRIM/files/original/cec9e08ab18ea585db4ff0d4c16eca0d.mei': 'CRIM_Mass_0004_1',
    'http://92.154.49.37/CRIM/files/original/e212991e0593a7c03c884b77d8cd868d.mei': 'CRIM_Mass_0004_2',
    'http://92.154.49.37/CRIM/files/original/1b598bb63c79e5cd5108bf2ea8283927.mei': 'CRIM_Mass_0004_3',
    'http://92.154.49.37/CRIM/files/original/48be2d1c5067cd75a553c58544101de4.mei': 'CRIM_Mass_0004_4',
    'http://92.154.49.37/CRIM/files/original/b8ab46f45ddbbad4ba5ab00e0200a416.mei': 'CRIM_Mass_0004_5',
    'http://92.154.49.37/CRIM/files/original/7a04e67f48cb3c1056301e598d4fd00e.mei': 'CRIM_Mass_0005_1',
    'http://92.154.49.37/CRIM/files/original/3ab294fd7121487a9d8da3e990d743a0.mei': 'CRIM_Mass_0005_2',
    'http://92.154.49.37/CRIM/files/original/cc3227b6304c4ca1e689be8507a0643a.mei': 'CRIM_Mass_0005_3',
    'http://92.154.49.37/CRIM/files/original/285a7682afcaa183419fad22218cf957.mei': 'CRIM_Mass_0005_4',
    'http://92.154.49.37/CRIM/files/original/31c7d33592876e5368b6c454c87fd8e7.mei': 'CRIM_Mass_0005_5',
    'http://92.154.49.37/CRIM/files/original/43e12f05ef4d7eb64a5e8db1e93caa80.mei': 'CRIM_Mass_0006_1',
    'http://92.154.49.37/CRIM/files/original/c2204856d2c8f340d387d42ac392ddf8.mei': 'CRIM_Mass_0006_2',
    'http://92.154.49.37/CRIM/files/original/1cef4cd106c727f64b7dd5a7df420f0f.mei': 'CRIM_Mass_0006_3',
    'http://92.154.49.37/CRIM/files/original/8a62abe58ae4ee037bc93d8cd5c7c4f6.mei': 'CRIM_Mass_0006_4',
    'http://92.154.49.37/CRIM/files/original/9b37d6dc5f0749748c48ac8e0f30d949.mei': 'CRIM_Mass_0006_5',
    'http://92.154.49.37/CRIM/files/original/8e2ab18bdadcc92dc6a45df7981eab03.mei': 'CRIM_Mass_0007_1',
    'http://92.154.49.37/CRIM/files/original/b577ccad489964864f3196948f33810a.mei': 'CRIM_Mass_0007_2',
    'http://92.154.49.37/CRIM/files/original/fda7fcc8e8fd0c70ceefa2d5d960c416.mei': 'CRIM_Mass_0007_3',
    'http://92.154.49.37/CRIM/files/original/3729aac97bd1bee5fe3f3eda65199a52.mei': 'CRIM_Mass_0007_4',
    'http://92.154.49.37/CRIM/files/original/2ffccac951b0829622b0633e9ac58207.mei': 'CRIM_Mass_0007_5',
    'http://92.154.49.37/CRIM/files/original/b982a8efdb5c4f95695f925681870b63.mei': 'CRIM_Mass_0008_1',
    'http://92.154.49.37/CRIM/files/original/f0d8df4918158b37d2855b4350539faf.mei': 'CRIM_Mass_0008_2',
    'http://92.154.49.37/CRIM/files/original/923f02f5f8f6bee216584f5ceba6018d.mei': 'CRIM_Mass_0008_3',
    'http://92.154.49.37/CRIM/files/original/3444e224df578164989360cc9b00d327.mei': 'CRIM_Mass_0008_4',
    'http://92.154.49.37/CRIM/files/original/e524a2b6b3710721367eccd42aad8e53.mei': 'CRIM_Mass_0008_5',
    'http://92.154.49.37/CRIM/files/original/6fb3bd785129d9e884d667d73232deea.mei': 'CRIM_Mass_0009_1',
    'http://92.154.49.37/CRIM/files/original/397ced78c2204727eda898a578494452.mei': 'CRIM_Mass_0009_2',
    'http://92.154.49.37/CRIM/files/original/47c9dc3c70fd86db9b49c252617de80f.mei': 'CRIM_Mass_0009_3',
    'http://92.154.49.37/CRIM/files/original/9aed0578764d9eaf734e0847fd48cdfd.mei': 'CRIM_Mass_0009_4',
    'http://92.154.49.37/CRIM/files/original/b5faad902ea15d4e31aa42f9290275ae.mei': 'CRIM_Mass_0009_5',
    'http://92.154.49.37/CRIM/files/original/9b8c0dba04c18ef6adfed673c9a88fbd.mei': 'CRIM_Mass_0010_1',
    'http://92.154.49.37/CRIM/files/original/377307d0d5e7a13baf3077a8eb555ab2.mei': 'CRIM_Mass_0010_2',
    'http://92.154.49.37/CRIM/files/original/751a101c1574f2ead1c738b1a423c830.mei': 'CRIM_Mass_0010_3',
    'http://92.154.49.37/CRIM/files/original/f96a6db25250083cc9e129cc7a05eae0.mei': 'CRIM_Mass_0010_4',
    'http://92.154.49.37/CRIM/files/original/7347edf538b3edbbf9919967df6e95ef.mei': 'CRIM_Mass_0010_5',
    'http://92.154.49.37/CRIM/files/original/dacc6cae420d354738558cbb3bec3379.mei': 'CRIM_Mass_0011_1',
    'http://92.154.49.37/CRIM/files/original/4ec44de9522b3205e89ba5f5b7f4a328.mei': 'CRIM_Mass_0011_2',
    'http://92.154.49.37/CRIM/files/original/517c1959aafaefab3034c2204bcbeda7.mei': 'CRIM_Mass_0011_3',
    'http://92.154.49.37/CRIM/files/original/e0b0b327cb191cdf6d5a03fe30ca840e.mei': 'CRIM_Mass_0011_4',
    'http://92.154.49.37/CRIM/files/original/b16f9f8cd86c10af2ac64e727f020f5a.mei': 'CRIM_Mass_0011_5',
    'http://92.154.49.37/CRIM/files/original/98f887585dba05d6f3234181d72baf64.mei': 'CRIM_Mass_0012_1',
    'http://92.154.49.37/CRIM/files/original/d7b1b6bd6fd3bfdba9b9045dd2e07130.mei': 'CRIM_Mass_0012_2',
    'http://92.154.49.37/CRIM/files/original/532fe474e2e22118929fb1e7018855f8.mei': 'CRIM_Mass_0012_3',
    'http://92.154.49.37/CRIM/files/original/5e7ff8d2bf55b3f9c2c885801c0b565a.mei': 'CRIM_Mass_0012_4',
    'http://92.154.49.37/CRIM/files/original/085f0f8be273f09b32e26776e9ea6fc8.mei': 'CRIM_Mass_0012_5',
    'http://92.154.49.37/CRIM/files/original/ad7892a25b222716ae1da56beac0f211.mei': 'CRIM_Mass_0013_1',
    'http://92.154.49.37/CRIM/files/original/3445fa225ce7b32bb041ccf0cd566a89.mei': 'CRIM_Mass_0013_2',
    'http://92.154.49.37/CRIM/files/original/665fe22019532726ddca838dbe13de22.mei': 'CRIM_Mass_0013_3',
    'http://92.154.49.37/CRIM/files/original/5fefb3bc53d8da0551c6324ce1861368.mei': 'CRIM_Mass_0013_4',
    'http://92.154.49.37/CRIM/files/original/1efbfb81cc93c149feb8aa8433d7350c.mei': 'CRIM_Mass_0013_5',
    'http://92.154.49.37/CRIM/files/original/1b7b354d4f272de1983c70cc4871d8cc.mei': 'CRIM_Mass_0014_1',
    'http://92.154.49.37/CRIM/files/original/b838c0c49ec78b1db74ed65c2b79767a.mei': 'CRIM_Mass_0014_2',
    'http://92.154.49.37/CRIM/files/original/d85ea3192f54731e1f2e8c2e7cd340c5.mei': 'CRIM_Mass_0014_3',
    'http://92.154.49.37/CRIM/files/original/046f1ae06da4d55067cea51e7deec470.mei': 'CRIM_Mass_0014_4',
    'http://92.154.49.37/CRIM/files/original/5feb23bc5d2be1f3c3a27d56bac587c6.mei': 'CRIM_Mass_0014_5',
    'http://92.154.49.37/CRIM/files/original/8365f28fe5b7153f4fd19aba70dc991d.mei': 'CRIM_Mass_0015_1',
    'http://92.154.49.37/CRIM/files/original/2948089d6cab8e3e632cbe1255b0bf64.mei': 'CRIM_Mass_0015_2',
    'http://92.154.49.37/CRIM/files/original/532f5cb2a0d75ce3afb971b24a875ad3.mei': 'CRIM_Mass_0015_3',
    'http://92.154.49.37/CRIM/files/original/c07431a4599bd858eeefba38e5731dd7.mei': 'CRIM_Mass_0015_4',
    'http://92.154.49.37/CRIM/files/original/7d304a2f1a833052ea2f4b9d342d8fc0.mei': 'CRIM_Mass_0015_5',
    'http://92.154.49.37/CRIM/files/original/def5d751e6d4a35a34e6665cd9004aaa.mei': 'CRIM_Mass_0016_1',
    'http://92.154.49.37/CRIM/files/original/d8064d0d82ee2a8532dc869500aae0dd.mei': 'CRIM_Mass_0016_2',
    'http://92.154.49.37/CRIM/files/original/7bfced971a2e95337bda9256cedd3bfe.mei': 'CRIM_Mass_0016_3',
    'http://92.154.49.37/CRIM/files/original/243f7b593e29af5724a1316f35d5a8a2.mei': 'CRIM_Mass_0016_4',
    'http://92.154.49.37/CRIM/files/original/5c9914a96f4e5478ff2373bd843d7be7.mei': 'CRIM_Mass_0016_5',
    'http://92.154.49.37/CRIM/files/original/73c7f0c7fc4f3521bdc478e2951b0d10.mei': 'CRIM_Mass_0017_1',
    'http://92.154.49.37/CRIM/files/original/f297f5c7e4487552bfe1b866cc367f7b.mei': 'CRIM_Mass_0017_2',
    'http://92.154.49.37/CRIM/files/original/08c1953f0ffd200214d822f7f862827f.mei': 'CRIM_Mass_0017_3',
    'http://92.154.49.37/CRIM/files/original/2d7311f5a3437942487d57cb8110b34d.mei': 'CRIM_Mass_0017_4',
    'http://92.154.49.37/CRIM/files/original/d9e50ed2d91bab0d5bc1bd218a2771be.mei': 'CRIM_Mass_0017_5',
    'http://92.154.49.37/CRIM/files/original/93f81b31408e3874cc34e7cc867a09c3.mei': 'CRIM_Mass_0018_1',
    'http://92.154.49.37/CRIM/files/original/9d36a9d520496d8a47df3aea1b4aeb72.mei': 'CRIM_Mass_0018_2',
    'http://92.154.49.37/CRIM/files/original/28f4d4f36b1a19866423a02989ab0eda.mei': 'CRIM_Mass_0018_3',
    'http://92.154.49.37/CRIM/files/original/898281c1b5f356cbccdddd116af81f45.mei': 'CRIM_Mass_0018_4',
    'http://92.154.49.37/CRIM/files/original/2e9b1b4866055b00ab43d14c291f3cb4.mei': 'CRIM_Mass_0018_5',
    'http://92.154.49.37/CRIM/files/original/b4be7b23f70de329c9b62acb3498d420.mei': 'CRIM_Mass_0019_1',
    'http://92.154.49.37/CRIM/files/original/80f3ec142b342eccd26644cecba4557b.mei': 'CRIM_Mass_0019_2',
    'http://92.154.49.37/CRIM/files/original/48f9063b8691a63c554c4e2cfaebb17c.mei': 'CRIM_Mass_0019_3',
    'http://92.154.49.37/CRIM/files/original/7cd5f8ae5da611f9bc2d28c2320d02db.mei': 'CRIM_Mass_0019_4',
    'http://92.154.49.37/CRIM/files/original/ad677d2e4b24b6cb26decf35190e3383.mei': 'CRIM_Mass_0019_5',
    'http://92.154.49.37/CRIM/files/original/238670bab93dc7918727ebc80ab188f3.mei': 'CRIM_Mass_0020_1',
    'http://92.154.49.37/CRIM/files/original/d12a01fddf568b9a0cd7b749bad24ab3.mei': 'CRIM_Mass_0020_2',
    'http://92.154.49.37/CRIM/files/original/997f74715356026155882fb698590d5e.mei': 'CRIM_Mass_0020_3',
    'http://92.154.49.37/CRIM/files/original/aef85c46b658265cfc7c92d2bf191236.mei': 'CRIM_Mass_0020_4',
    'http://92.154.49.37/CRIM/files/original/6c3ef83527cc29e84061dfe152399c45.mei': 'CRIM_Mass_0020_5',
    'http://92.154.49.37/CRIM/files/original/e9937cb1dcf2bc349852dba567393e0a.mei': 'CRIM_Model_0001',
    'http://92.154.49.37/CRIM/files/original/8c82de7d89635ff85cdf8f547b1eb44e.mei': 'CRIM_Model_0002',
    'http://92.154.49.37/CRIM/files/original/2665e1a34fe3a29877b492112ca72551.mei': 'CRIM_Model_0003',
    'http://92.154.49.37/CRIM/files/original/3451f0235054a756c1f4e8c5674f6e7d.mei': 'CRIM_Model_0004',
    'http://92.154.49.37/CRIM/files/original/4a24ccb45a7e9275f9bb4eb980dbb000.mei': 'CRIM_Model_0005',
    'http://92.154.49.37/CRIM/files/original/8299f01ad2aa1c2871c2cd614074dbf3.mei': 'CRIM_Model_0006',
    'http://92.154.49.37/CRIM/files/original/a1bb3de28bcbb5830319ed3a3f01ae6a.mei': 'CRIM_Model_0007',
    'http://92.154.49.37/CRIM/files/original/78a288aa8141dc2953ee850ee379d7dd.mei': 'CRIM_Model_0008',
    'http://92.154.49.37/CRIM/files/original/6b8fdf8ba21f385bf2e3cd4725a1cf9f.mei': 'CRIM_Model_0009',
    'http://92.154.49.37/CRIM/files/original/e43fdbfa635aac6d653dd21c0a51cc76.mei': 'CRIM_Model_0010',
    'http://92.154.49.37/CRIM/files/original/90375cb1ddfe9cf8ba7d7e866f9a0611.mei': 'CRIM_Model_0011',
    'http://92.154.49.37/CRIM/files/original/b81e93fba20eeee757c11be63d651a95.mei': 'CRIM_Model_0012',
    'http://92.154.49.37/CRIM/files/original/8f713a7ab2f3d9d5b0c2a439d96e05b7.mei': 'CRIM_Model_0013',
    'http://92.154.49.37/CRIM/files/original/e0bd90d0802a546e0c47fd66121ce36a.mei': 'CRIM_Model_0014',
    'http://92.154.49.37/CRIM/files/original/9684b93e8f954b7eb2fe5b3ba1bab6f5.mei': 'CRIM_Model_0015',
    'http://92.154.49.37/CRIM/files/original/1552fc4d83c3d312f170933bc41dc2c7.mei': 'CRIM_Model_0016',
    'http://92.154.49.37/CRIM/files/original/4d6d7ef6c83cc1cf2f11da3cd73b70f0.mei': 'CRIM_Model_0017',
    'http://92.154.49.37/CRIM/files/original/360f2456072c989fc0e3dd042303d1dc.mei': 'CRIM_Model_0018',
    'http://92.154.49.37/CRIM/files/original/ea2cde97dfec4e00e047d2a04a2edf85.mei': 'CRIM_Model_0019',
    'http://92.154.49.37/CRIM/files/original/5406198189b92e47e9f60b58f10f56fb.mei': 'CRIM_Model_0020',
    'http://92.154.49.37/CRIM/files/original/363de758819de36532c306bcf35c1db3.mei': 'CRIM_Model_0021',
    'http://92.154.49.37/CRIM/files/original/f9dce15ced481fa04a9b191fbb3c97f7.mei': 'CRIM_Model_0022',
    'http://92.154.49.37/CRIM/files/original/7b426e2d6d275534aa001abff1d9e687.mei': 'CRIM_Model_0023',
    'http://92.154.49.37/CRIM/files/original/410fb1a662c87ee71ac75f6f2fc960e8.mei': 'CRIM_Model_0024',
}


def add_single_voice(piece_id, original_name, regularized_name, order, data):
    new_voice_fields = OrderedDict()
    new_voice_fields['voice_id'] = '{0}({1})'.format(piece_id, order)
    new_voice_fields['piece'] = piece_id
    new_voice_fields['original_name'] = original_name if original_name != '~' else ''
    new_voice_fields['regularized_name'] = regularized_name if regularized_name != '~' else ''
    new_voice_fields['order'] = order

    new_voice_row = {
        'model': 'crim.crimvoice',
        'fields': new_voice_fields,
    }
    data.append(new_voice_row)


def process_voices(csvfile):
    '''Takes a csv file, rearranges the data as appropriate
    for the CRIM Django site, and exports the data as an
    OrderedDict.'''
    data = []
    # idgen = count()
    csvreader = csv.DictReader(csvfile)
    for old_row in csvreader:
        piece_id = LINKS_TO_PIECE_ID[old_row['MEI link']]
        original_voice_names = old_row['Original voice names'].split('|')
        regularized_voice_names = old_row['Regularized voice names'].split('|')

        for i in range(len(original_voice_names)):
            add_single_voice(piece_id, original_voice_names[i], regularized_voice_names[i], i+1, data)

    return data


if __name__ == '__main__':
    with open(FILE_IN, encoding='utf-8', newline='') as csvfile:
        data = process_voices(csvfile)
    with open(FILE_OUT, 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(data))
