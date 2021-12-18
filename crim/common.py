from crim.models.definition import CRIMDefinition

try:
    CURRENT_DEFINITION = CRIMDefinition.objects.latest('id')
except:
    CURRENT_DEFINITION = CRIMDefinition(
        observation_definition={},
        relationship_definition={},
    )
