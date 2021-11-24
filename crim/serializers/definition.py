from rest_framework import serializers
from crim.models.definition import CRIMDefinition

class CRIMDefinitionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimdefinition-detail-data', lookup_field='id')

    class Meta:
        model = CRIMDefinition
        fields = (
            'url',
            'id',
            'observation_definition',
            'relationship_definition',
            'remarks',
            'created',
            'updated',
            'curated',
        )
