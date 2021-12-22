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

    return render(request, 'relationship/relationship_form.html',
                  context={'form': form,
                           'relationship_definition': get_current_definition().relationship_definition,
                           'observation_definition': get_current_definition().observation_definition,
                           'all_pieces': CRIMPiece.objects.order_by('piece_id'),
                           'current_definition_id': get_current_definition().id,
                          },
                 )
