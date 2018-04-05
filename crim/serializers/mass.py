from crim.models.piece import CRIMMass
from crim.models.role import CRIMRole
from rest_framework import serializers


class CRIMRoleMassSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMRole
        fields = (
            'url',
            'person',
            'role_type',
            'date',
        )


class CRIMMassListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMMass
        fields = (
            'url',
            'title',
            'genre',
            'people',
        )


class CRIMMassDetailSerializer(serializers.HyperlinkedModelSerializer):
#     Add mass movements to serialized mass
#     movements = serializers.HyperlinkedRelatedField(
#         many=True,
#         read_only=True,
#         view='crimmassmovement-detail',
#     )
    roles = CRIMRoleMassSummarySerializer(
        many=True,
        read_only=True,
        source='roles_as_mass',
    )

    class Meta:
        model = CRIMMass
        fields = (
            'url',
            'title',
            'genre',
            'roles',
            # 'movements',
            'remarks',
        )
