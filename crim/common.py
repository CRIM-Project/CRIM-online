from crim.models.definition import CRIMDefinition
from crim.models.voice import CRIMVoice

from django.utils.html import conditional_escape

def get_current_definition():
    try:
        return CRIMDefinition.objects.latest('id')
    except:
        return CRIMDefinition(
            observation_definition={},
            relationship_definition={},
        )

def print_voice(piece_id, voice_number):
    try:
        v = CRIMVoice.objects.get(piece=piece_id, order=voice_number)
        # If there is an original voice name, use that;
        # otherwise, use the regularized name.
        if v.original_name:
            name_to_use = v.original_name
        else:
            name_to_use = f'[{v.regularized_name}]'
        return (conditional_escape(str(voice_number)) +
                ': ' +
                conditional_escape(name_to_use)
               )
    except:
        if voice_number:
            return ('<span style="color:#c71a22;">' +
                    conditional_escape(str(voice_number)) +
                    '</span>'
                   )
        else:
            return conditional_escape('-')
