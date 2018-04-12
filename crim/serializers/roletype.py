from crim.models.role import CRIMRoleType
from rest_framework import serializers


class CRIMRoleTypeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimroletype-detail', lookup_field='role_type_id')

    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'name',
            'remarks',
        )
