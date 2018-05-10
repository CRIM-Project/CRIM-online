from crim.models.part import CRIMPart
from rest_framework import serializers


class CRIMPartSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpart-detail', lookup_field='part_id')

    class Meta:
        model = CRIMPart
        fields = (
            'url',
            'piece',
            'name',
            'order',
            'remarks',
        )
