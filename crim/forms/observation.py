from django import forms
from crim.models.observation import CJObservation
from crim.models.definition import CRIMDefinition

from crim.common import *

# PIECE_CHOICES = (
#    ('1', 'Piece 1'),
#    ('2', 'Piece 2'),
#    ('3', 'Piece 3'),
#    ('4', 'Piece 4'),
# )

allowed_types = list(CURRENT_DEFINITION.observation_definition.keys())
# MUSICAL_TYPE_CHOICES = []
# strkey = ''
# for type in allowed_types:
#    strkey = str(type).capitalize()
#    MUSICAL_TYPE_CHOICES.append((strkey, strkey))

class ObservationForm(forms.ModelForm):
    # piece = forms.ChoiceField(choices=PIECE_CHOICES)

    class Meta:
        model = CJObservation
        fields = ['observer', 'musical_type', 'details', 'definition']
        widgets = {
            'definition': forms.HiddenInput(),
            'details': forms.HiddenInput(),
        }

    # def __init__(self, *args, **kwargs):
    #    super(ObservationForm, self).__init__(*args, **kwargs)
    #    self.fields['musical_type'] = forms.ChoiceField(choices=MUSICAL_TYPE_CHOICES)
