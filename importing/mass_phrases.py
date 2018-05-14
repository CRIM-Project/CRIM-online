import csv
import json
import os

from collections import OrderedDict
from crim.common import two_digit_string

PATH_IN = 'source/mass_phrases'
FILE_IN_LIST = os.listdir(PATH_IN)
FILE_OUT = '../crim/fixtures/mass_phrases.json'

MASS_ORDINARY = {
    "Kyrie eleison.": "Lord, have mercy.",
    "Christe eleison.": "Christ, have mercy.",
    "Et in terra pax hominibus bonae voluntatis.": "And in earth peace to men of good will.",
    "Laudamus te.": "We praise thee.",
    "Benedicimus te.": "We bless thee.",
    "Adoramus te.": "We worship thee.",
    "Glorificamus te.": "We glorify thee.",
    "Gratias agimus tibi propter magnam gloriam tuam.": "We give thanks to thee for thy great glory.",
    "Domine Deus, Rex caelestis, Deus Pater omnipotens.": "Lord God, Heavenly King, God the Father Almighty.",
    "Domine Fili unigenite Iesu Christe.": "Lord Jesus Christ, the only begotten Son.",
    "Domine Deus, Agnus Dei, Filius Patris.": "Lord God, Lamb of God, Son of the Father.",
    "Qui tollis peccata mundi, miserere nobis.": "Thou that takest away the sins of the world, have mercy upon us.",
    "Qui tollis peccata mundi, suscipe deprecationem nostram.": "Thou that takest away the sins of the world, receive our prayer.",
    "Qui sedes ad dexteram Patris, miserere nobis.": "Thou that sittest at the right hand of the Father, have mercy upon us.",
    "Quoniam tu solus sanctus.": "For thou only art holy.",
    "Tu solus Dominus.": "Thou only art the Lord.",
    "Tu solus Altissimus, Iesu Christe.": "Thou only art the most high, Jesus Christ.",
    "Cum Sancto Spiritu, in gloria Dei Patris.": "With the Holy Ghost, in the glory of God the Father.",
    "Amen.": "Amen.",
    "Patrem omnipotentem, factorem caeli et terrae, visibilium omnium, et invisibilium.": "The Father almighty, maker of heaven and earth, and of all things visible and invisible.",
    "Et in unum Dominum Iesum Christum, Filium Dei unigenitum.": "And in one Lord Jesus Christ, the only begotten Son of God.",
    "Et ex Patre natum ante omnia saecula.": "Begotten of the Father before all worlds.",
    "Deum de Deo, lumen de lumine, Deum verum de Deo vero.": "God of God, light of light, true God of true God.",
    "Genitum, non factum, consubstantialem Patri:": "Begotten, not made, being of one substance with the Father.",
    "per quem omnia facta sunt.": "by whom all things were made.",
    "Qui propter non homines, et propter nostram salutem descendit de caelis.": "Who for us men and for our salvation came down from heaven.",
    "Et incarnatus est de Spiritu Sancto ex Maria Virgine:": "And was incarnate by the Holy Ghost of the Virgin Mary.",
    "Et homo factus est.": "And was made man.",
    "Crucifixus etiam pro nobis:": "He was crucified also for us:",
    "sub Pontio Pilato passus, et sepultus est.": "he suffered under Pontius Pilate, and was buried.",
    "Et resurrexit tertia die, secundum Scripturas.": "And on the third day He rose again, according to the Scriptures.",
    "Et ascendit in caelum:": "And ascended into heaven:",
    "sedet ad dexteram Patris.": "he sitteth at the right hand of the Father.",
    "Et iterum venturus est cum gloria, iudicare vivos et mortuos:": "And He shall come again with glory, to judge the living and the dead:",
    "cuius regni non erit finis.": "whose kingdom shall have no end.",
    "Et in Spiritum Sanctum, Dominum, et vivificantem:": "And in the Holy Ghost, the Lord and giver of life:",
    "qui ex Patre Filioque procedit.": "who prodeedeth from the Father and the Son.",
    "Qui cum Patre et Filio simul adoratur, et conglorificatur:": "Who with the Father and the Son together is worshipped and glorified:",
    "qui locutus est per Prophetas.": "who spake by the Prophets.",
    "Et unam sanctam catholicam et apostolicam Ecclesiam.": "And in one holy catholic and apostolic Church.",
    "Confiteor unum baptisma in remissionem peccatorum.": "I acknowledge one Baptism for the remission of sins.",
    "Et expecto resurrectionem mortuorum.": "And I look for the resurrection of the dead.",
    "Et vitam venturi saeculi.": "And the life of the world to come.",
    "Sanctus Dominus Deus Sabaoth.": "Holy, holy, holy, Lord God of Hosts.",
    "Pleni sunt caeli et terra gloria tua.": "Heaven and earth are full of thy glory.",
    "Hosanna in excelsis.": "Hosanna in the highest.",
    "Benedictus qui venit in nomine Domini.": "Blessed is he that cometh in the name of the Lord.",
    "Agnus Dei, qui tollis peccata mundi:": "Lamb of God, that takest away the sins of the world:",
    "miserere nobis.": "have mercy upon us.",
    "dona nobis pacem.": "grant us thy peace.",
    "Spiritus et alme orphanorum Paraclete.": "Spirit and bounteous Comforter of orphans.",
    "Primogenitus Mariae Virginis Matris.": "Firstborn of the Virgin Mother Mary.",
    "Ad Mariae gloriam.": "To the glory of Mary.",
    "Mariam sanctificans.": "Sanctifying Mary.",
    "Mariam gubernans.": "Governing Mary.",
    "Tu solus Altissimus, Mariam coronans, Iesu Christe.": "Thou only art the most high, crowning Mary, Jesus Christ.",
    "Benedictus Mariae Filius qui venit in nomine Domini.": "Blessed is the Son of Mary who cometh in the name of the Lord.",
    "[Quoniam] tu solus sanctus.": "[For] thou only art holy.",
}


def add_phrase(old_row, new_fields):
    part_with_default = old_row['Part'] if old_row['Part'] else '1'
    new_fields['phrase_id'] = old_row['Mass_Section_ID'] + ':' + two_digit_string(old_row['Section_Phrase_Number'])
    new_fields['piece'] = old_row['Mass_Section_ID']
    new_fields['part'] = old_row['Mass_Section_ID'] + '.' + part_with_default
    new_fields['number'] = eval(old_row['Section_Phrase_Number'])
    new_fields['start_measure'] = eval(old_row['Start_Measure'])
    new_fields['stop_measure'] = eval(old_row['Stop_Measure'])
    new_fields['text'] = old_row['Text']
    new_fields['translation'] = MASS_ORDINARY[old_row['Text']]


def add_part(old_row, new_fields, existing_parts):
    part_with_default = old_row['Part'] if old_row['Part'] else '1'
    part_id = old_row['Mass_Section_ID'] + '.' + part_with_default
    if part_id in existing_parts:
        pass
    else:
        new_fields['part_id'] = part_id
        new_fields['piece'] = old_row['Mass_Section_ID']
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
