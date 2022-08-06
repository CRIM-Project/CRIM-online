from crim.models.observation import CJObservation
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json

from crim.forms.relationship import RelationshipForm
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
