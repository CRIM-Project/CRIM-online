from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import json

from crim.forms.relationship import RelationshipForm
from crim.models import relationship
from crim.models.relationship import CJRelationship
from crim.models.observation import CJObservation
from crim.models.definition import CRIMDefinition
from crim.models.piece import CRIMPiece

from crim.common import get_current_definition


def get_relationship(request):
    form = RelationshipForm(initial={"definition": get_current_definition()})

    current_def = get_current_definition()
    singular_voice_fields = current_def.voice_fields['singular']
    plural_voice_fields = current_def.voice_fields['plural']
    singular_voice_fields_hyphens = [x.replace(' ', '-') for x in singular_voice_fields]
    plural_voice_fields_hyphens = [x.replace(' ', '-') for x in plural_voice_fields]

    return render(request, 'relationship/relationship_form.html',
                  context={'form': form,
                           'relationship_definition': current_def.relationship_definition,
                           'observation_definition': current_def.observation_definition,
                           'singular_voice_fields': singular_voice_fields_hyphens,
                           'plural_voice_fields': plural_voice_fields_hyphens,
                           'all_pieces': CRIMPiece.objects.order_by('piece_id'),
                           'current_definition_id': current_def.id,
                          },
                 )

def edit_relationship(request, id):
    relationship = get_object_or_404(CJRelationship, id = id)
    
    curr_user = request.user
    # Deny users access to editing models they do not own
    if not curr_user.is_superuser and (curr_user.profile.person.id != relationship.observer_id):
        return HttpResponseRedirect(f"/relationships/{id}/")

    form = RelationshipForm(initial={"definition": relationship.definition}, instance = relationship)

    if request.method == 'PATCH':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f"/relationships/{id}/")
        # else:
            # TODO: Return to the form with a validation error

    current_def = relationship.definition
    if None == current_def:
        return render(request, 'relationship/error.html',
                      context = {   'form': form,
                                    'back_url': f'/relationships/{ relationship.id }/',
                                    'relationship': relationship,
                                },
                    )

    singular_voice_fields = current_def.voice_fields['singular']
    plural_voice_fields = current_def.voice_fields['plural']
    singular_voice_fields_hyphens = [x.replace(' ', '-') for x in singular_voice_fields]
    plural_voice_fields_hyphens = [x.replace(' ', '-') for x in plural_voice_fields]

    return render(request, 'relationship/relationship_edit.html',
                  context={ 'form': form,
                            'back_url': f'/relationships/{ relationship.id }/',
                            'relationship': relationship,
                            'relationship_definition': current_def.relationship_definition,
                            'observation_definition': current_def.observation_definition,
                            'singular_voice_fields': singular_voice_fields_hyphens,
                            'plural_voice_fields': plural_voice_fields_hyphens,
                            'all_pieces': CRIMPiece.objects.order_by('piece_id'),
                            'current_definition_id': current_def.id,
                          },
                 )

def copy_relationship(request, id):
    relationship = get_object_or_404(CJRelationship, id = id)

    form = RelationshipForm(initial={"definition": relationship.definition}, instance = relationship)

    if request.method == 'PATCH':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f"/relationships/{id}/")
        # else:
            # TODO: Return to the form with a validation error

    current_def = relationship.definition
    if None == current_def:
        return render(request, 'relationship/error.html',
                      context = {   'form': form,
                                    'back_url': f'/relationships/{ relationship.id }/',
                                    'copy': True,
                                    'relationship': relationship,
                                },
                    )
    
    singular_voice_fields = current_def.voice_fields['singular']
    plural_voice_fields = current_def.voice_fields['plural']
    singular_voice_fields_hyphens = [x.replace(' ', '-') for x in singular_voice_fields]
    plural_voice_fields_hyphens = [x.replace(' ', '-') for x in plural_voice_fields]

    return render(request, 'relationship/relationship_edit.html',
                  context={ 'form': form,
                            'back_url': f'/relationships/{ relationship.id }/',
                            'copy': True,
                            'relationship': relationship,
                            'relationship_definition': current_def.relationship_definition,
                            'observation_definition': current_def.observation_definition,
                            'singular_voice_fields': singular_voice_fields_hyphens,
                            'plural_voice_fields': plural_voice_fields_hyphens,
                            'all_pieces': CRIMPiece.objects.order_by('piece_id'),
                            'current_definition_id': current_def.id,
                          },
                 )

def __get_relationship(observation):
    models = list(observation.observations_as_model.all())
    derivs = list(observation.observations_as_derivative.all())
    if len(models) > 0:
        return models[0]
    if len(derivs) > 0:
        return derivs[0]
    return None

def edit_observation(request, id):
    observation = get_object_or_404(CJObservation, id = id)
    relationship = __get_relationship(observation)

    form = RelationshipForm(initial={"definition": relationship.definition}, instance = relationship)

    if request.method == 'PATCH':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f"/relationships/{id}/")
        # else:
            # TODO: Return to the form with a validation error

    current_def = relationship.definition
    if None == current_def:
        return render(request, 'relationship/error.html',
                      context = {   'form': form,
                                    'back_url': f'/observations/{ observation.id }/',
                                    'relationship': relationship,
                                },
                    )

    singular_voice_fields = current_def.voice_fields['singular']
    plural_voice_fields = current_def.voice_fields['plural']
    singular_voice_fields_hyphens = [x.replace(' ', '-') for x in singular_voice_fields]
    plural_voice_fields_hyphens = [x.replace(' ', '-') for x in plural_voice_fields]

    return render(request, 'relationship/relationship_edit.html',
                  context={ 'form': form,
                            'back_url': f'/observations/{ observation.id }/',
                            'relationship': relationship,
                            'relationship_definition': current_def.relationship_definition,
                            'observation_definition': current_def.observation_definition,
                            'singular_voice_fields': singular_voice_fields_hyphens,
                            'plural_voice_fields': plural_voice_fields_hyphens,
                            'all_pieces': CRIMPiece.objects.order_by('piece_id'),
                            'current_definition_id': current_def.id,
                          },
                 )

def __create_relationship(observation):
    relationship_data = {}
    relationship_data['observer'] = observation.observer

    models = list(observation.observations_as_model.all())
    derivs = list(observation.observations_as_derivative.all())
    relationship_data['model_observation'] = CJObservation()
    relationship_data['derivative_observation'] = CJObservation()
    if len(models) > 0:
        relationship_data['model_observation'] = observation
    if len(derivs) > 0:
        relationship_data['derivative_observation'] = observation

    relationship_data['definition'] = observation.definition

    return CJRelationship(**relationship_data)

def copy_observation(request, id):
    observation = get_object_or_404(CJObservation, id = id)
    relationship = __create_relationship(observation)

    form = RelationshipForm(initial={"definition": relationship.definition}, instance = relationship)

    if request.method == 'PATCH':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f"/relationships/{id}/")
        # else:
            # TODO: Return to the form with a validation error

    current_def = relationship.definition
    if None == current_def:
        return render(request, 'relationship/error.html',
                      context = {   'form': form,
                                    'back_url': f'/observations/{ observation.id }/',
                                    'copy': True,
                                    'relationship': relationship,
                                },
                    )

    singular_voice_fields = current_def.voice_fields['singular']
    plural_voice_fields = current_def.voice_fields['plural']
    singular_voice_fields_hyphens = [x.replace(' ', '-') for x in singular_voice_fields]
    plural_voice_fields_hyphens = [x.replace(' ', '-') for x in plural_voice_fields]

    return render(request, 'relationship/relationship_edit.html',
                  context={ 'form': form,
                            'copy': True,
                            'back_url': f'/observations/{ observation.id }/',
                            'relationship': relationship,
                            'relationship_definition': current_def.relationship_definition,
                            'observation_definition': current_def.observation_definition,
                            'singular_voice_fields': singular_voice_fields_hyphens,
                            'plural_voice_fields': plural_voice_fields_hyphens,
                            'all_pieces': CRIMPiece.objects.order_by('piece_id'),
                            'current_definition_id': current_def.id,
                          },
                 )
