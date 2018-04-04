from crim.models.mass import CRIMMass
from crim.models.piece import CRIMPiece
from crim.models.document import CRIMTreatise, CRIMSource
from crim.models.role import CRIMRole
from rest_framework import serializers


class CRIMRoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMRole
        fields = (
            'url',
            'person',
            'role_type',
            'date',
            'piece',
            #             'mass',
            #             'treatise',
            #             'source',
            'remarks',
        )
