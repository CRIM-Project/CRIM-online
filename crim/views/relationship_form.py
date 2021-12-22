from crim.models.observation import CJObservation
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json

from crim.forms.relationship import RelationshipForm
from crim.models.definition import CRIMDefinition
from crim.models.piece import CRIMPiece

from crim.common import *


def get_relationship(request):
    form = RelationshipForm(initial={"definition": CURRENT_DEFINITION})

    return render(request, 'relationship/relationship_form.html',
                  context={'form': form,
                           'relationship_definition': CURRENT_DEFINITION.relationship_definition,
                           'observation_definition': CURRENT_DEFINITION.observation_definition,
                           'all_pieces': CRIMPiece.objects.order_by('piece_id'),
                          },
                 )
