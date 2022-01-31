from django import forms
#from splitjson.widgets import SplitJSONWidget
from crim.models.relationship import CJRelationship
from crim.models.definition import CRIMDefinition
from crim.models.observation import CJObservation

from crim.common import *

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
