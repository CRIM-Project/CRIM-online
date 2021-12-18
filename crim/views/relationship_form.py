from crim.models.observation import CJObservation
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json

from crim.forms.relationship import RelationshipForm
from crim.forms.observation import ObservationForm
from crim.models.definition import CRIMDefinition

from crim.common import *

def make_new_observation(request, prefix, allowed_types, definition):
    musical_type = ''
    obs_details_dict = {}
    selected_type = request.POST[prefix+'selected-tab']
    strip1 = ''.join(e for e in selected_type if e.isalnum()) #get name of active type

    for selected_type in allowed_types:
        strip2 = ''.join(e for e in selected_type if e.isalnum()) #get name of each allowed type
        if strip1 == strip2: #if same type
            musical_type = musical_type + selected_type #set musical type
            allowed_subtypes = list(definition.observation_definition[selected_type]) #allowed subtype for it
            for subtype in allowed_subtypes: #get name of each allowed subtype
                slug = prefix + selected_type + '-' + subtype.replace(' ', '-')

                # check if checkboxes need to be added to array
                if slug in dict(request.POST):
                    if request.POST[slug] != "":
                        obs_details_dict[subtype.capitalize()] = request.POST[slug].capitalize()
                    else:
                        obs_details_dict[subtype.capitalize()] = "None"
                # if checkboxes to be input as array
                else:
                    allowed_options = list(definition.observation_definition[selected_type][subtype]['checkbox'])
                    selected_options = []
                    for option in allowed_options:
                        slug_array = prefix + selected_type + '-' + option.replace(' ', '-').lower()
                        if slug_array in dict(request.POST):
                            selected_options.append(request.POST[slug_array])
                        selected_options_string = ', '.join([str(elem) for elem in selected_options])
                        obs_details_dict[subtype.capitalize()] = selected_options_string
            break

    obs_json_object = json.dumps(obs_details_dict)
    obs_form_data = {'observer' : request.POST['observer'],
                    'musical_type' : musical_type.capitalize(),
                    'details': obs_json_object,
                    'definition': definition}
    obs_form = ObservationForm(obs_form_data)
    return obs_form


def get_relationship(request):
    # if this is a POST request we need to process the form data
    if request.is_ajax and request.method == 'POST':
        # create a form instance and manually populate it with data from the request:
        details_dict = {}
        relationship_type = ''
        all_forms_valid = False

        #RELATIONSHIP DETAILS
        allowed_types = list(CURRENT_DEFINITION.relationship_definition.keys())
        selected_type = request.POST['selected-tab']
        strip1 = ''.join(e for e in selected_type if e.isalnum()) #get name of active type

        for rtype in allowed_types:
            strip2 = ''.join(e for e in rtype if e.isalnum()) #get name of each allowed type
            if strip1 == strip2: #if same type
                relationship_type = relationship_type + rtype #set rela type
                allowed_subtypes = list(CURRENT_DEFINITION.relationship_definition[rtype]) #allowed subtype for it
                if len(allowed_subtypes) != 0:
                    for subtype in allowed_subtypes: #get name of each allowed subtype
                        slug = selected_type + '-' + subtype.replace(' ', '-')
                        details_dict[subtype.capitalize()] = request.POST[slug]
                else:
                    details_dict={}
                break
        json_object = json.dumps(details_dict)
        print("details dict of this rela: " + str(json_object))

        #OBSERVATION DETAILS
        #both existing observation
        if request.POST['model_observation'] != "" and request.POST['derivative_observation'] != "":
            form_data = {"observer": request.POST['observer'],
                        "relationship_type": relationship_type.capitalize(),
                        "details": json_object,
                        "model_observation": request.POST['model_observation'],
                        "derivative_observation": request.POST['derivative_observation'],
                        "definition": CURRENT_DEFINITION
                        }
            all_forms_valid = True

        #observation(s) made new
        else:
            observation_allowed_types = list(CURRENT_DEFINITION.observation_definition.keys())

            #model existing and derivative made new
            if request.POST['model_observation'] != "" and request.POST['derivative_observation'] == "":
                derivative_form = make_new_observation(request, "derivative-", observation_allowed_types, CURRENT_DEFINITION)

                if derivative_form.is_valid():
                    derivative_form.save()

                    form_data = {"observer": request.POST['observer'],
                                "relationship_type": relationship_type.capitalize(),
                                "details": json_object,
                                "model_observation": request.POST['model_observation'],
                                "derivative_observation": CJObservation.objects.latest('id'),
                                "definition": CURRENT_DEFINITION
                                }
                    all_forms_valid = True

            #model made new and derivative existing
            elif request.POST['model_observation'] == "" and request.POST['derivative_observation'] != "":
                model_form = make_new_observation(request, "model-", observation_allowed_types, CURRENT_DEFINITION)

                if model_form.is_valid():
                    model_form.save()

                    form_data = {"observer": request.POST['observer'],
                                "relationship_type": relationship_type.capitalize(),
                                "details": json_object,
                                "model_observation": CJObservation.objects.latest('id'),
                                "derivative_observation": request.POST['derivative_observation'],
                                "definition": CURRENT_DEFINITION
                                }
                    all_forms_valid = True

            #both made new
            else:
                model_form = make_new_observation(request, "model-", observation_allowed_types, CURRENT_DEFINITION)
                derivative_form = make_new_observation(request, "derivative-", observation_allowed_types, CURRENT_DEFINITION)

                if model_form.is_valid() and derivative_form.is_valid():
                    model_form.save()
                    derivative_form.save()

                    form_data = {"observer": request.POST['observer'],
                                "relationship_type": relationship_type.capitalize(),
                                "details": json_object,
                                "model_observation": CJObservation.objects.all().order_by('-id')[1],
                                "derivative_observation": CJObservation.objects.latest('id'),
                                "definition": CURRENT_DEFINITION
                                }
                    all_forms_valid = True

        form = RelationshipForm(form_data)

        if all_forms_valid and form.is_valid():
            form.save()


    # if a GET (or any other method) we'll create a blank form
    else:
        form = RelationshipForm(initial={"definition": CURRENT_DEFINITION})

    return render(request, 'relationship/relationship_form.html',
                context={'form': form,
                        'relationship_definition': CURRENT_DEFINITION.relationship_definition,
                        'observation_definition': CURRENT_DEFINITION.observation_definition
                        })
