from crim.models.relationship import CRIMRelationshipType
from rest_framework import serializers


class CRIMRelationshipTypeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrelationshiptype-detail', lookup_field='relationship_type_id')

    class Meta:
        model = CRIMRelationshipType
        fields = (
            'url',
            'name',
            'remarks',
        )
