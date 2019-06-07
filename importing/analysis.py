import json
import os
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crim.settings')
import django

from importing.analysis_constants import *

django.setup()

FILE_IN = 'source/batch2/newbatch-peeled.json'
FILE_OUT = '../crim/fixtures/reimport.json'
NUMBERED_OUT = 'source/batch2/reimport-numbered.json'
UNPROCESSED_OUT = 'source/batch2/reimport-unprocessed.json'
LOG = 'source/batch2/reimport-log.txt'
OBSERVATION_COUNT = 0
RELATIONSHIP_COUNT = 0

# TODO: add "needs review" if has a same created_date as another one.
# TODO: collapse duplicate observations.


def process_json():
    '''Given an input file, write imported json to `new_fixture`, and
    put any unimported json in `unprocessed_json`.
    '''
    processed_data = []
    unprocessed_data = []
    log = []
    with open(FILE_IN, encoding='utf-8', newline='') as old_json_file:
        old_data = json.load(old_json_file)
    for item in old_data:
        handle_item(item, processed_data, unprocessed_data, log)
    with open(NUMBERED_OUT, 'w', encoding='utf-8') as numbered_file:
        # `old_data` has been updated with <R0> numbers
        numbered_file.write(json.dumps(old_data, indent=2))
    with open(FILE_OUT, 'w', encoding='utf-8') as new_fixture:
        new_fixture.write(json.dumps(processed_data))
    with open(UNPROCESSED_OUT, 'w', encoding='utf-8') as unprocessed_json_file:
        unprocessed_json_file.write(json.dumps(unprocessed_data, indent=2))
    with open(LOG, 'w', encoding='utf-8') as log_file:
        log_file.write('\n'.join(log))


def clean_timestamp(s):
    ss = s.replace('::', ':00:')
    return re.sub(':$', '', ss)


def handle_item(item, processed_data, unprocessed_data, log):
    if eval(item['user']) not in USERS_TO_KEEP:
        leave_unprocessed(item, unprocessed_data, log, 'User {0} not in list of approved analysts.'.format(item['user']))
    elif 'relationships' not in item or not item['relationships']:
        leave_unprocessed(item, unprocessed_data, log, 'No relationships in item.')
    else:
        create_item(item, processed_data, unprocessed_data, log)


def leave_unprocessed(item, unprocessed_data, log, fault):
    item['fault'] = fault
    unprocessed_data.append(item)
    log.append('Item with timestamp {0} unproccesed: {1}'.format(item['created_at'], fault))


def create_item(item, processed_data, unprocessed_data, log):
    global RELATIONSHIP_COUNT
    possible_relationships = []
    for relationship in item['relationships']:
        if not relationship['types']:
            log.append('Relationship with timestamp {} unprocessed: null type'.format(item['created_at']))
        else:
            possible_relationships.append(relationship)
    if not possible_relationships:
        leave_unprocessed(item, unprocessed_data, log, 'No relationships with timestamp {}'.format(item['created_at']))
        return
    else:
        for relationship_to_process in possible_relationships:
            new_observations = create_observations(item, relationship_to_process, processed_data, unprocessed_data, log)
            new_relationship_fields = {}
            if new_observations:
                model_observation_fields, derivative_observation_fields = new_observations
                new_relationship_fields['observer'] = PEOPLE[item['user']]
                new_relationship_fields['model_observation'] = model_observation_fields['id']
                new_relationship_fields['derivative_observation'] = derivative_observation_fields['id']
                new_relationship_fields['model_piece'] = model_observation_fields['piece']
                new_relationship_fields['derivative_piece'] = derivative_observation_fields['piece']
                new_relationship_fields['created'] = clean_timestamp(item['created_at'])
                new_relationship_fields['updated'] = clean_timestamp(item['created_at'])
                new_relationship_fields['curated'] = False if 'needs_review' in item and item['needs_review'] else True
                model_observation_fields['curated'] = new_relationship_fields['curated']
                derivative_observation_fields['curated'] = new_relationship_fields['curated']
                add_relationship_types(relationship_to_process, new_relationship_fields)

                model_observation_row = {
                    'model': 'crim.crimobservation',
                    'fields': model_observation_fields,
                    'pk': model_observation_fields['id'],
                }
                derivative_observation_row = {
                    'model': 'crim.crimobservation',
                    'fields': derivative_observation_fields,
                    'pk': derivative_observation_fields['id'],
                }
                RELATIONSHIP_COUNT += 1
                relationship_to_process['relationship_id'] = '<R{}>'.format(RELATIONSHIP_COUNT)
                new_relationship_row = {
                    'model': 'crim.crimrelationship',
                    'fields': new_relationship_fields,
                    'pk': RELATIONSHIP_COUNT,
                }
                processed_data.append(model_observation_row)
                processed_data.append(derivative_observation_row)
                processed_data.append(new_relationship_row)
            else:
                return


def create_observations(item, relationship, processed_data, unprocessed_data, log):
    global OBSERVATION_COUNT
    '''Create an observation for each observation in the old data.
    Use cids to link relationships to the proper observations.
    '''
    model_observation = {}
    derivative_observation = {}

    if 'CRIM_Model' in PIECES[relationship['titleA']] and 'CRIM_Mass' in PIECES[relationship['titleB']]:
        relationship['boolDir'] = True
    elif 'CRIM_Mass' in PIECES[relationship['titleA']] and 'CRIM_Model' in PIECES[relationship['titleB']]:
        relationship['boolDir'] = False

    if not relationship['titleA']:
        log.append('No titleA for relationship with timestamp {}'.format(item['created_at']))
    if not relationship['titleB']:
        log.append('No titleB for relationship with timestamp {}'.format(item['created_at']))
    if not relationship['scoreA_ema']:
        log.append('No scoreA_ema for relationship with timestamp {}'.format(item['created_at']))
    if not relationship['scoreB_ema']:
        log.append('No scoreB_ema for relationship with timestamp {}'.format(item['created_at']))

    if relationship['boolDir']:
        model_observation['piece'] = PIECES[relationship['titleA']]
        derivative_observation['piece'] = PIECES[relationship['titleB']]
        model_observation['ema'] = relationship['scoreA_ema']
        derivative_observation['ema'] = relationship['scoreB_ema']
    else:
        model_observation['piece'] = PIECES[relationship['titleB']]
        derivative_observation['piece'] = PIECES[relationship['titleA']]
        model_observation['ema'] = relationship['scoreB_ema']
        derivative_observation['ema'] = relationship['scoreA_ema']

    model_observation['observer'] = PEOPLE[item['user']]
    derivative_observation['observer'] = PEOPLE[item['user']]
    model_observation['created'] = clean_timestamp(item['created_at'])
    derivative_observation['created'] = clean_timestamp(item['created_at'])
    model_observation['updated'] = clean_timestamp(item['created_at'])
    derivative_observation['updated'] = clean_timestamp(item['created_at'])

    # If looking up the observation in the item's observations
    # returns a result, use that data to add a type to the observation;
    # also copy the remarks. Otherwise, these fields simply aren't added.
    if 'assertions' in item:
        if 'scoreAassert' in relationship:
            for observation in item['assertions']:
                if observation['cid'] == relationship['scoreAassert']:
                    if relationship['boolDir']:
                        add_musical_types(observation, model_observation)
                    else:
                        add_musical_types(observation, derivative_observation)
        if 'scoreBassert' in relationship:
            for observation in item['assertions']:
                if observation['cid'] == relationship['scoreBassert']:
                    if relationship['boolDir']:
                        add_musical_types(observation, derivative_observation)
                    else:
                        add_musical_types(observation, model_observation)

    # Finally, return the new observations with unique ids.
    OBSERVATION_COUNT += 1
    model_observation['id'] = OBSERVATION_COUNT
    OBSERVATION_COUNT += 1
    derivative_observation['id'] = OBSERVATION_COUNT
    return (model_observation, derivative_observation)


def add_orphan_observation(item, observation, processed_data):
    global OBSERVATION_COUNT

    new_observation_fields = {}
    new_observation_fields['piece'] = PIECES[observation['title']]
    new_observation_fields['ema'] = observation['ema']

    new_observation_fields['observer'] = PEOPLE[item['user']]
    new_observation_fields['created'] = clean_timestamp(item['created_at'])
    new_observation_fields['updated'] = clean_timestamp(item['created_at'])
    new_observation_fields['curated'] = False

    OBSERVATION_COUNT += 1
    new_observation_row = {
        'model': 'crim.crimobservation',
        'pk': OBSERVATION_COUNT,
        'fields': new_observation_fields,
    }
    processed_data.append(new_observation_row)


def _add_list_as_string(item, base_name='voice'):
    combined_list = []
    count = 1
    while base_name + str(count) in item:
        combined_list.append(item[base_name + str(count)])
        count += 1
    return '\n'.join(combined_list)


def _get_from_options(list_of_dicts, k):
    for d in list_of_dicts:
        if k in d:
            return d[k]


def add_musical_types(observation, new_observation):
    '''Add the musical types and remarks of an observation to the
    new observation object.'''
    new_observation['remarks'] = observation['comment']
    if 'mt-cf' in observation['types']:
        new_observation['mt_cf'] = True
        new_observation['mt_cf_voices'] = _add_list_as_string(observation['types']['mt-cf']['options'])
        new_observation['mt_cf_dur'] = observation['types']['mt-cf']['dur']
        new_observation['mt_cf_mel'] = observation['types']['mt-cf']['mel']
    if 'mt-sog' in observation['types']:
        new_observation['mt_sog'] = True
        new_observation['mt_sog_voices'] = _add_list_as_string(observation['types']['mt-sog']['options'])
        new_observation['mt_sog_dur'] = observation['types']['mt-sog']['dur']
        new_observation['mt_sog_mel'] = observation['types']['mt-sog']['mel']
        new_observation['mt_sog_ostinato'] = observation['types']['mt-sog']['ost']
        new_observation['mt_sog_periodic'] = observation['types']['mt-sog']['per']
    if 'mt-csog' in observation['types']:
        new_observation['mt_csog'] = True
        new_observation['mt_csog_voices'] = _add_list_as_string(observation['types']['mt-csog']['options'])
        new_observation['mt_csog_dur'] = observation['types']['mt-csog']['dur']
        new_observation['mt_csog_mel'] = observation['types']['mt-csog']['mel']
    if 'mt-cd' in observation['types']:
        new_observation['mt_cd'] = True
        new_observation['mt_cd_voices'] = _add_list_as_string(observation['types']['mt-cd']['options'])
    if 'mt-fg' in observation['types']:
        new_observation['mt_fg'] = True
        new_observation['mt_fg_voices'] = _add_list_as_string(observation['types']['mt-fg']['options'])
        new_observation['mt_fg_int'] = observation['types']['mt-fg']['int']
        new_observation['mt_fg_tint'] = observation['types']['mt-fg']['tint']
        new_observation['mt_fg_periodic'] = observation['types']['mt-fg']['pe']
        new_observation['mt_fg_strict'] = observation['types']['mt-fg']['ste']
        new_observation['mt_fg_flexed'] = observation['types']['mt-fg']['fe']
        new_observation['mt_fg_sequential'] = observation['types']['mt-fg']['se']
        new_observation['mt_fg_inverted'] = observation['types']['mt-fg']['ie']
        new_observation['mt_fg_retrograde'] = observation['types']['mt-fg']['re']
    if 'mt-pe' in observation['types']:
        new_observation['mt_pe'] = True
        new_observation['mt_pe_voices'] = _add_list_as_string(observation['types']['mt-pe']['options'])
        new_observation['mt_pe_int'] = observation['types']['mt-pe']['int']
        new_observation['mt_pe_tint'] = observation['types']['mt-pe']['tint']
        new_observation['mt_pe_strict'] = observation['types']['mt-pe']['ste']
        new_observation['mt_pe_flexed'] = observation['types']['mt-pe']['fe']
        new_observation['mt_pe_flt'] = observation['types']['mt-pe']['fte']
        new_observation['mt_pe_sequential'] = observation['types']['mt-pe']['se']
        new_observation['mt_pe_added'] = observation['types']['mt-pe']['ae']
        new_observation['mt_pe_invertible'] = observation['types']['mt-pe']['ic']
    if 'mt-id' in observation['types']:
        new_observation['mt_id'] = True
        new_observation['mt_id_voices'] = _add_list_as_string(observation['types']['mt-id']['options'])
        new_observation['mt_id_int'] = observation['types']['mt-id']['int']
        new_observation['mt_id_tint'] = observation['types']['mt-id']['tint']
        new_observation['mt_id_strict'] = observation['types']['mt-id']['ste']
        new_observation['mt_id_flexed'] = observation['types']['mt-id']['fe']
        new_observation['mt_id_flt'] = observation['types']['mt-id']['fte']
        new_observation['mt_id_invertible'] = observation['types']['mt-id']['ic']
    if 'mt-nid' in observation['types']:
        new_observation['mt_nid'] = True
        new_observation['mt_nid_voices'] = _add_list_as_string(observation['types']['mt-nid']['options'])
        new_observation['mt_nid_int'] = observation['types']['mt-nid']['int']
        new_observation['mt_nid_tint'] = observation['types']['mt-nid']['tint']
        new_observation['mt_nid_strict'] = observation['types']['mt-nid']['ste']
        new_observation['mt_nid_flexed'] = observation['types']['mt-nid']['fe']
        new_observation['mt_nid_flt'] = observation['types']['mt-nid']['fte']
        new_observation['mt_nid_sequential'] = observation['types']['mt-nid']['se']
        new_observation['mt_nid_invertible'] = observation['types']['mt-nid']['ic']
    if 'mt-hr' in observation['types']:
        new_observation['mt_hr'] = True
        new_observation['mt_hr_voices'] = _add_list_as_string(observation['types']['mt-hr']['options'])
        new_observation['mt_hr_simple'] = observation['types']['mt-hr']['s']
        new_observation['mt_hr_staggered'] = observation['types']['mt-hr']['st']
        new_observation['mt_hr_sequential'] = observation['types']['mt-hr']['se']
        new_observation['mt_hr_fauxbourdon'] = observation['types']['mt-hr']['fa']
    if 'mt-cad' in observation['types']:
        new_observation['mt_cad'] = True
        new_observation['mt_cad_cantizans'] = _get_from_options(observation['types']['mt-cad']['options'], 'voice1')
        new_observation['mt_cad_tenorizans'] = _get_from_options(observation['types']['mt-cad']['options'], 'voice2')
        if observation['types']['mt-cad']['a']:
            assert not observation['types']['mt-cad']['ph'] and not observation['types']['mt-cad']['p']
            new_observation['mt_cad_type'] = 'authentic'
        elif observation['types']['mt-cad']['ph']:
            assert not observation['types']['mt-cad']['a'] and not observation['types']['mt-cad']['p']
            new_observation['mt_cad_type'] = 'phrygian'
        elif observation['types']['mt-cad']['p']:
            assert not observation['types']['mt-cad']['a'] and not observation['types']['mt-cad']['ph']
            new_observation['mt_cad_type'] = 'plagal'
        new_observation['mt_cad_tone'] = observation['types']['mt-cad']['tone']
        new_observation['mt_cad_dtv'] = _get_from_options(observation['types']['mt-cad']['options'], 'dove_voice1')
        new_observation['mt_cad_dti'] = observation['types']['mt-cad']['dove']
    if 'mt-int' in observation['types']:
        new_observation['mt_int'] = True
        new_observation['mt_int_voices'] = _add_list_as_string(observation['types']['mt-int']['options'])
        new_observation['mt_int_p6'] = observation['types']['mt-int']['p6']
        new_observation['mt_int_p3'] = observation['types']['mt-int']['p3']
        new_observation['mt_int_c35'] = observation['types']['mt-int']['c35']
        new_observation['mt_int_c83'] = observation['types']['mt-int']['c83']
        new_observation['mt_int_c65'] = observation['types']['mt-int']['c65']
    if 'mt-fp' in observation['types']:
        new_observation['mt_fp'] = True
        new_observation['mt_fp_ir'] = observation['types']['mt-fp']['ir']
        new_observation['mt_fp_range'] = observation['types']['mt-fp']['r']
        new_observation['mt_fp_comment'] = observation['types']['mt-fp']['text']


def add_relationship_types(old_relationship, new_relationship):
    '''Add the relationship types and remarks of an relationship to the
    new relationship object.'''
    new_relationship['remarks'] = old_relationship['comment']
    if 'rt-q' in old_relationship['types']:
        new_relationship['rt_q'] = True
        new_relationship['rt_q_x'] = old_relationship['types']['rt-q']['ex']
        new_relationship['rt_q_monnayage'] = old_relationship['types']['rt-q']['mo']
    if 'rt-tm' in old_relationship['types']:
        new_relationship['rt_tm'] = True
        new_relationship['rt_tm_snd'] = old_relationship['types']['rt-tm']['snd']
        new_relationship['rt_tm_minv'] = old_relationship['types']['rt-tm']['minv']
        new_relationship['rt_tm_retrograde'] = old_relationship['types']['rt-tm']['r']
        new_relationship['rt_tm_ms'] = old_relationship['types']['rt-tm']['ms']
        new_relationship['rt_tm_transposed'] = old_relationship['types']['rt-tm']['t']
        new_relationship['rt_tm_invertible'] = old_relationship['types']['rt-tm']['td']
    if 'rt-tnm' in old_relationship['types']:
        new_relationship['rt_tnm'] = True
        new_relationship['rt_tnm_embellished'] = old_relationship['types']['rt-tnm']['em']
        new_relationship['rt_tnm_reduced'] = old_relationship['types']['rt-tnm']['re']
        new_relationship['rt_tnm_amplified'] = old_relationship['types']['rt-tnm']['am']
        new_relationship['rt_tnm_truncated'] = old_relationship['types']['rt-tnm']['tr']
        new_relationship['rt_tnm_ncs'] = old_relationship['types']['rt-tnm']['ncs']
        new_relationship['rt_tnm_ocs'] = old_relationship['types']['rt-tnm']['ocs']
        new_relationship['rt_tnm_ocst'] = old_relationship['types']['rt-tnm']['ocst'] if 'ocst' in old_relationship['types']['rt-tnm'] else False
        new_relationship['rt_tnm_nc'] = old_relationship['types']['rt-tnm']['nc']
    if 'rt-nm' in old_relationship['types']:
        new_relationship['rt_nm'] = True
    if 'rt-om' in old_relationship['types']:
        new_relationship['rt_om'] = True


if __name__ == '__main__':
    process_json()
