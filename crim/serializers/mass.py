from crim.models.genre import CRIMGenre
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMMass
from crim.models.role import CRIMRoleType, CRIMRole
from rest_framework import serializers


class CRIMRoleTypeMassSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'name',
        )


class CRIMGenreMassSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMGenre
        fields = (
            'url',
            'name',
        )


class CRIMPersonMassSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMPerson
        fields = (
            'url',
            'name',
        )


class CRIMRoleMassSummarySerializer(serializers.HyperlinkedModelSerializer):
    person = CRIMPersonMassSummarySerializer(read_only=True)
    role_type = CRIMRoleTypeMassSummarySerializer(read_only=True)

    class Meta:
        model = CRIMRole
        fields = (
            'url',
            'person',
            'role_type',
            'date',
        )


class CRIMMassListSerializer(serializers.HyperlinkedModelSerializer):
    genre = CRIMGenreMassSummarySerializer(read_only=True)
    roles = CRIMRoleMassSummarySerializer(
        many=True,
        read_only=True,
        source='roles_as_mass',
    )

    class Meta:
        model = CRIMMass
        fields = (
            'url',
            'mass_id',
            'title',
            'genre',
            'roles',
            'remarks',
        )


class CRIMMassDetailSerializer(serializers.HyperlinkedModelSerializer):
#     Add mass movements to serialized mass
#     movements = serializers.HyperlinkedRelatedField(
#         many=True,
#         read_only=True,
#         view='crimmassmovement-detail',
#     )
    genre = CRIMGenreMassSummarySerializer(read_only=True)
    roles = CRIMRoleMassSummarySerializer(
        many=True,
        read_only=True,
        source='roles_as_mass',
    )

    class Meta:
        model = CRIMMass
        fields = (
            'url',
            'mass_id',
            'title',
            'genre',
            'roles',
            # 'movements',
            'remarks',
        )
