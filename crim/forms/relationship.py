from django import forms
#from splitjson.widgets import SplitJSONWidget
from crim.models.relationship import CJRelationship
from crim.models.definition import CRIMDefinition
from crim.models.observation import CJObservation

from crim.common import *

# PIECE_CHOICES = (
#    ('1', 'Piece 1'),
#    ('2', 'Piece 2'),
#    ('3', 'Piece 3'),
#    ('4', 'Piece 4'),
# )

allowed_types = list(CURRENT_DEFINITION.relationship_definition.keys())
# RELATIONSHIP_TYPE_CHOICES = []
# strkey = ''
# for type in allowed_types:
#    strkey = str(type).capitalize()
#    RELATIONSHIP_TYPE_CHOICES.append((strkey, strkey))

class RelationshipForm(forms.ModelForm):
    # piece = forms.ChoiceField(choices=PIECE_CHOICES)
    # details = forms.CharField(required=False)

    class Meta:
        model = CJRelationship
        fields = [
            'observer',
            'relationship_type',
            'details',
            'model_observation',
            'derivative_observation',
            'definition',
        ]
        # widgets = {
        #     'definition': forms.HiddenInput(),
        #     'details': forms.HiddenInput(),
        # }

    def __init__(self, *args, **kwargs):
        super(RelationshipForm, self).__init__(*args, **kwargs)
        self.fields['model_observation'] = forms.ModelChoiceField(
                queryset=CJObservation.objects.all(),
                required=False,
            )
        self.fields['derivative_observation'] = forms.ModelChoiceField(
                queryset=CJObservation.objects.all(),
                required=False,
            )
        self.fields['model_observation'].label = ''
        self.fields['derivative_observation'].label = ''
