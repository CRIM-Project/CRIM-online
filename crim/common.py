from crim.models.definition import CRIMDefinition
from crim.models.voice import CRIMVoice

def get_current_definition():
    try:
        return CRIMDefinition.objects.latest('id')
    except:
        return CRIMDefinition(
            observation_definition={},
            relationship_definition={},
        )

def get_voice_name_from_number(piece_id, voice_number):
    try:
        v = CRIMVoice.objects.get(piece=piece_id, order=voice_number)
        return v.original_name
    except:
        return str(voice_number)
