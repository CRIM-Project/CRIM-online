from crim.models.mass import CRIMMass
from crim.models.piece import CRIMPiece
from crim.models.document import CRIMTreatise, CRIMSource
from crim.models.role import CRIMRole
from rest_framework import serializers


class CRIMRoleSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrole-detail', lookup_field='pk')

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
