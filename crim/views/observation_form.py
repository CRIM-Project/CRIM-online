from django.http import HttpResponse
from django.shortcuts import render
import json
from crim.forms.observation import ObservationForm
from crim.models.observation import CJObservation
from django.contrib import messages

from crim.common import *

def get_observation(request):
    # if this is a POST request we need to process the form data
    if request.is_ajax and request.method == 'POST':
        # create a form instance and manually populate it with data from the request:
        details_dict = {}
        musical_type = ''

        allowed_types = list(CURRENT_DEFINITION.observation_definition.keys())
        selected_type = request.POST['selected-tab']
        strip1 = ''.join(e for e in selected_type if e.isalnum()) #get name of active type

        for mtype in allowed_types:
            strip2 = ''.join(e for e in mtype if e.isalnum()) #get name of each allowed type
            if strip1 == strip2: #if same type
                musical_type = musical_type + mtype #set musical type
                allowed_subtypes = list(CURRENT_DEFINITION.observation_definition[mtype]) #allowed subtype for it
                for subtype in allowed_subtypes: #get name of each allowed subtype
                    slug = selected_type + '-' + subtype.replace(' ', '-')

                    # check if checkboxes need to be added to array
                    if slug in dict(request.POST):
                        if request.POST[slug] != "":
                            details_dict[subtype.capitalize()] = request.POST[slug].capitalize()
                        else:
                            details_dict[subtype.capitalize()] = "None"
                    # if checkboxes to be input as array
                    else:
                        allowed_options = list(CURRENT_DEFINITION.observation_definition[mtype][subtype]['checkbox'])
                        selected_options = []
                        for option in allowed_options:
                            slug_array = selected_type + '-' + option.replace(' ', '-').lower()
                            if slug_array in dict(request.POST):
                                selected_options.append(request.POST[slug_array])
                        selected_options_string = ', '.join([str(elem) for elem in selected_options])
                        details_dict[subtype.capitalize()] = selected_options_string
                break
        json_object = json.dumps(details_dict)

        form_data = {"observer": request.POST['observer'],
                    "musical_type": musical_type.capitalize(),
                    "details": json_object,
                    "definition": CURRENT_DEFINITION
                    }
        #print(form_data)
        form = ObservationForm(form_data)
        #print (form.is_bound)
        #print (form.is_valid())
        #print (form.errors)
        #print (form.non_field_errors)
        # check whether it's valid:
        if form.is_valid():
            form.save()
        messages.success(request, 'You just created observation #' + CJObservation.objects.latest('id').__str__())

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ObservationForm(initial={"definition": CURRENT_DEFINITION})

    context_to_return = {
        'form': form,
        'observation_definition': CURRENT_DEFINITION.observation_definition,
    }
    return render(request, 'observation/observation_form.html', context=context_to_return)
