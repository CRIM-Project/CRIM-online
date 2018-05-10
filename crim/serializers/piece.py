from crim.models.document import CRIMSource
from crim.models.genre import CRIMGenre
from crim.models.mass import CRIMMass
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece
from crim.models.role import CRIMRoleType, CRIMRole
from rest_framework import serializers


class CRIMRoleTypePieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimroletype-detail', lookup_field='role_type_id')

    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'name',
        )


class CRIMGenrePieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimgenre-detail', lookup_field='genre_id')

    class Meta:
        model = CRIMGenre
        fields = (
            'url',
            'name',
        )


class CRIMPersonPieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimperson-detail', lookup_field='person_id')

    class Meta:
        model = CRIMPerson
        fields = (
            'url',
            'name',
        )


class CRIMRolePieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrole-detail', lookup_field='pk')
    person = CRIMPersonPieceSerializer(read_only=True)
    role_type = CRIMRoleTypePieceSerializer(read_only=True)

    class Meta:
        model = CRIMRole
        fields = (
            'url',
            'person',
            'role_type',
            'date',
            'remarks',
        )


class CRIMMassMovementPieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='crimpiece-detail',
        lookup_field='piece_id',
    )

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
        )


class CRIMMassPieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='crimmass-detail',
        lookup_field='mass_id',
    )
    roles = CRIMRolePieceSerializer(
        many=True,
        read_only=True,
        source='roles_as_mass',
    )
    movements = CRIMMassMovementPieceSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = CRIMMass
        fields = (
            'url',
            'mass_id',
            'title',
            'roles',
            'movements',
        )


class CRIMSourcePieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='crimsource-detail',
        lookup_field='document_id',
    )
    roles = CRIMRolePieceSerializer(
        many=True,
        read_only=True,
        source='roles_as_source',
    )

    class Meta:
        model = CRIMSource
        fields = (
            'url',
            'document_id',
            'title',
            'roles',
        )


class CRIMPieceListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail', lookup_field='piece_id')
    roles = CRIMRolePieceSerializer(
        many=True,
        read_only=True,
        source='roles_as_piece',
    )
    mass = CRIMMassPieceSerializer(read_only=True)
    genre = CRIMGenrePieceSerializer(read_only=True)
    # unique_roles = serializers.SerializerMethodField()

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'genre',
            'mass',
            'number_of_voices',
            'roles',
            'pdf_links',
            'mei_links',
            'remarks',
        )


class CRIMPieceDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail', lookup_field='piece_id')
    roles = CRIMRolePieceSerializer(
        many=True,
        read_only=True,
        source='roles_as_piece',
    )
    mass = CRIMMassPieceSerializer(read_only=True)
    genre = CRIMGenrePieceSerializer(read_only=True)
    sources = CRIMSourcePieceSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'genre',
            'mass',
            'number_of_voices',
            'roles',
            'sources',
            'pdf_links',
            'mei_links',
            'remarks',
        )
