from crim.models.document import CRIMTreatise, CRIMSource
from crim.models.genre import CRIMGenre
from crim.models.mass import CRIMMass
from crim.models.observation import CRIMObservation
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece
from crim.models.role import CRIMRoleType, CRIMRole
from rest_framework import serializers

ANALYST = 'Analyst'


class CRIMGenrePersonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimgenre-detail-data', lookup_field='genre_id')

    class Meta:
        model = CRIMGenre
        fields = (
            'url',
            'name',
        )


class CRIMRoleTypePersonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimroletype-detail-data', lookup_field='role_type_id')

    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'role_type_id',
            'name',
        )


class CRIMMassPersonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimmass-detail-data', lookup_field='mass_id')
    genre = CRIMGenrePersonSerializer(read_only=True)

    class Meta:
        model = CRIMMass
        fields = (
            'url',
            'title',
            'genre',
        )


class CRIMPiecePersonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')
    genre = CRIMGenrePersonSerializer(read_only=True)

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'full_title',
            'genre',
            'date',
        )


class CRIMTreatisePersonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimtreatise-detail-data', lookup_field='document_id')

    class Meta:
        model = CRIMTreatise
        fields = (
            'url',
            'title',
        )


class CRIMSourcePersonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimsource-detail-data', lookup_field='document_id')

    class Meta:
        model = CRIMSource
        fields = (
            'url',
            'title',
        )


class CRIMRolePersonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrole-detail-data', lookup_field='id')
    mass = CRIMMassPersonSerializer(read_only=True)
    piece = CRIMPiecePersonSerializer(read_only=True)
    treatise = CRIMTreatisePersonSerializer(read_only=True)
    source = CRIMSourcePersonSerializer(read_only=True)
    role_type = CRIMRoleTypePersonSerializer(read_only=True)

    class Meta:
        model = CRIMRole
        fields = (
            'url',
            'role_type',
            'date',
            'mass',
            'piece',
            'treatise',
            'source',
            'remarks',
        )


class CRIMPersonListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimperson-detail-data', lookup_field='person_id')
    role_types = CRIMRoleTypePersonSerializer(many=True, read_only=True)

    class Meta:
        model = CRIMPerson
        fields = (
            'url',
            'person_id',
            'name',
            'name_sort',
            'name_alternate_list',
            'birth_date',
            'death_date',
            'active_date',
            'role_types',
        )


class CRIMPersonDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimperson-detail-data', lookup_field='person_id')
    role_types = CRIMRoleTypePersonSerializer(many=True, read_only=True)
    roles = CRIMRolePersonSerializer(many=True, read_only=True)

    class Meta:
        model = CRIMPerson
        fields = (
            'url',
            'person_id',
            'name',
            'name_sort',
            'name_alternate_list',
            'birth_date',
            'death_date',
            'active_date',
            'role_types',
            'remarks',
            'roles',
        )
