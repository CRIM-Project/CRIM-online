from crim.models.relationship import CRIMRelationship
from rest_framework import serializers


class CRIMRelationshipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMRelationship
        fields = (
            'url',
            'observer',
            'relationship_type',
            'model',
            'model_ema',
            'model_musical_types',
            'derivative',
            'derivative_ema',
            'derivative_musical_types',
            'remarks',
            'created',
            'updated',
        )