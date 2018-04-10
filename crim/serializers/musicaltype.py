from crim.models.relationship import CRIMMusicalType
from rest_framework import serializers


class CRIMMusicalTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMMusicalType
        fields = (
            'url',
            'name',
            'remarks',
        )
