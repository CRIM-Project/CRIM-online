from crim.models.genre import CRIMGenre
from crim.models.mass import CRIMMass
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece
from crim.models.role import CRIMRoleType, CRIMRole
from rest_framework import serializers


class CRIMRoleTypeMassSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimroletype-detail', lookup_field='role_type_id')

    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'name',
        )


class CRIMGenreMassSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimgenre-detail', lookup_field='genre_id')

    class Meta:
        model = CRIMGenre
        fields = (
            'url',
            'name',
        )


class CRIMPersonMassSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimperson-detail', lookup_field='person_id')

    class Meta:
        model = CRIMPerson
        fields = (
            'url',
            'name',
        )


class CRIMRoleMassSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrole-detail', lookup_field='pk')
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


class CRIMPieceMassSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail', lookup_field='piece_id')

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'pdf_links',
            'mei_links',
        )


class CRIMMassListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimmass-detail', lookup_field='mass_id')
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
    url = serializers.HyperlinkedIdentityField(view_name='crimmass-detail', lookup_field='mass_id')
    genre = CRIMGenreMassSummarySerializer(read_only=True)
    roles = CRIMRoleMassSummarySerializer(
        many=True,
        read_only=True,
        source='roles_as_mass',
    )
    movements = CRIMPieceMassSummarySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = CRIMMass
        fields = (
            'url',
            'mass_id',
            'title',
            'genre',
            'roles',
            'movements',
            'remarks',
        )
