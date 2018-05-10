from crim.models.role import CRIMRole
from rest_framework import serializers


class CRIMRoleSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrole-detail-data', lookup_field='pk')

    class Meta:
        model = CRIMRole
        fields = (
            'url',
            'person',
            'role_type',
            'date',
            'mass',
            'piece',
            'treatise',
            'source',
            'remarks',
        )
