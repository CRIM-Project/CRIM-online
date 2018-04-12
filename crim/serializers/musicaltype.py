from crim.models.relationship import CRIMMusicalType
from rest_framework import serializers


class CRIMMusicalTypeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimmusicaltype-detail', lookup_field='musical_type_id')

    class Meta:
        model = CRIMMusicalType
        fields = (
            'url',
            'name',
            'remarks',
        )
