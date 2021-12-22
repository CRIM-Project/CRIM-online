from crim.models.definition import CRIMDefinition

def get_current_definition():
    try:
        return CRIMDefinition.objects.latest('id')
    except:
        return CRIMDefinition(
            observation_definition={},
            relationship_definition={},
        )
