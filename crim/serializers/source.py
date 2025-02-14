from crim.models.genre import CRIMGenre
from crim.models.person import CRIMPerson
from crim.models.mass import CRIMMass
from crim.models.piece import CRIMPiece
from crim.models.role import CRIMRoleType, CRIMRole
from crim.models.document import CRIMTreatise, CRIMSource
from rest_framework import serializers


class CRIMGenreSourceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimgenre-detail-data', lookup_field='genre_id')

    class Meta:
        model = CRIMGenre
        fields = (
            'url',
            'name',
        )


class CRIMRoleTypeSourceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimroletype-detail-data', lookup_field='role_type_id')

    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'role_type_id',
            'name',
        )


class CRIMPersonSourceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimperson-detail-data', lookup_field='person_id')

    class Meta:
        model = CRIMPerson
        fields = (
            'url',
            'name',
        )


class CRIMRoleSourceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrole-detail-data', lookup_field='id')
    person = CRIMPersonSourceSerializer(read_only=True)
    role_type = CRIMRoleTypeSourceSerializer(read_only=True)

    class Meta:
        model = CRIMRole
        fields = (
            'url',
            'person',
            'role_type',
            'date',
        )


class CRIMMassSourceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimmass-detail-data', lookup_field='mass_id')
    composer = CRIMPersonSourceSerializer(read_only=True)

    class Meta:
        model = CRIMMass
        fields = (
            'url',
            'mass_id',
            'title',
            'genre',
            'composer',
            'date',
            'remarks',
        )


class CRIMPieceSourceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')
    composer = CRIMPersonSourceSerializer(read_only=True)
    genre = CRIMGenreSourceSerializer(read_only=True)

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'genre',
            'composer',
            'date',
            'remarks',
        )


class CRIMTreatiseSourceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimtreatise-detail-data', lookup_field='document_id')
    author = CRIMPersonSourceSerializer(read_only=True)

    class Meta:
        model = CRIMTreatise
        fields = (
            'url',
            'document_id',
            'title',
            'author',
            'date',
            'remarks',
        )


class CRIMSourceListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimsource-detail-data', lookup_field='document_id')
    publisher = CRIMPersonSourceSerializer(read_only=True)
    external_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMSource
        fields = (
            'url',
            'document_id',
            'title',
            'publisher',
            'date',
            'date_sort',
            'external_links',
            'remarks',
        )

    def get_external_links(self, obj):
        return obj.external_links.split('\n') if obj.external_links else []


class CRIMSourceDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimsource-detail-data', lookup_field='document_id')
    mass_contents = CRIMMassSourceSerializer(
        many=True,
        read_only=True,
    )
    piece_contents = CRIMPieceSourceSerializer(
        many=True,
        read_only=True,
    )
    treatise_contents = CRIMTreatiseSourceSerializer(
        many=True,
        read_only=True,
    )
    roles = CRIMRoleSourceSerializer(
        many=True,
        read_only=True,
        source='roles_as_source',
    )
    external_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMSource
        fields = (
            'url',
            'document_id',
            'title',
            'roles',
            'external_links',
            'mass_contents',
            'piece_contents',
            'treatise_contents',
            'remarks',
        )

    def get_external_links(self, obj):
        return obj.external_links.split('\n') if obj.external_links else []
