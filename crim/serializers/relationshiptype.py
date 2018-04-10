from crim.models.relationship import CRIMRelationshipType
from rest_framework import serializers


class CRIMRelationshipTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMRelationshipType
        fields = (
            'url',
            'name',
            'remarks',
        )
