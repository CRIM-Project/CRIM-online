from crim.models.document import CRIMTreatise, CRIMSource
from crim.models.genre import CRIMGenre
from crim.models.mass import CRIMMass
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece
from crim.models.role import CRIMRoleType, CRIMRole
from rest_framework import serializers


class CRIMGenrePersonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimgenre-detail', lookup_field='genre_id')

    class Meta:
        model = CRIMGenre
        fields = (
            'url',
            'name',
        )


class CRIMRoleTypePersonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimroletype-detail', lookup_field='role_type_id')

    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'name',
        )


class CRIMMassPersonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimmass-detail', lookup_field='mass_id')
    genre = CRIMGenrePersonSerializer(read_only=True)

    class Meta:
        model = CRIMMass
        fields = (
            'url',
            'title',
            'genre',
        )


class CRIMPiecePersonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail', lookup_field='piece_id')
    genre = CRIMGenrePersonSerializer(read_only=True)

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'title',
            'genre',
        )


class CRIMTreatisePersonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimtreatise-detail', lookup_field='document_id')

    class Meta:
        model = CRIMTreatise
        fields = (
            'url',
            'title',
        )


class CRIMSourcePersonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimsource-detail', lookup_field='document_id')

    class Meta:
        model = CRIMSource
        fields = (
            'url',
            'title',
        )


class CRIMRolePersonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrole-detail', lookup_field='pk')
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
    def get_unique_roles(self, obj):
        unique_roles = []
        crimroles = CRIMRole.objects.filter(person=obj)
        for crimrole in crimroles:
            if crimrole.role_type:
                role_type_name = crimrole.role_type.name
                if role_type_name not in unique_roles:
                    unique_roles.append(role_type_name)
        unique_roles.sort()
        return unique_roles

    url = serializers.HyperlinkedIdentityField(view_name='crimperson-detail', lookup_field='person_id')
    unique_roles = serializers.SerializerMethodField()

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
            'unique_roles',
        )


class CRIMPersonDetailSerializer(serializers.HyperlinkedModelSerializer):
    def get_unique_roles(self, obj):
        unique_roles = []
        crimroles = CRIMRole.objects.filter(person=obj)
        for crimrole in crimroles:
            if crimrole.role_type:
                role_type_name = crimrole.role_type.name
                if role_type_name not in unique_roles:
                    unique_roles.append(role_type_name)
        unique_roles.sort()
        return unique_roles

    url = serializers.HyperlinkedIdentityField(view_name='crimperson-detail', lookup_field='person_id')
    unique_roles = serializers.SerializerMethodField()
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
            'remarks',
            'roles',
            'unique_roles',
        )
