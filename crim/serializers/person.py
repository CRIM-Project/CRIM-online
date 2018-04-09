from crim.models.document import CRIMTreatise, CRIMSource
from crim.models.genre import CRIMGenre
from crim.models.mass import CRIMMass
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece
from crim.models.role import CRIMRoleType, CRIMRole
from rest_framework import serializers


class CRIMGenrePersonSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMGenre
        fields = (
            'url',
            'name',
        )


class CRIMRoleTypePersonSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'name',
        )


class CRIMMassPersonSummarySerializer(serializers.HyperlinkedModelSerializer):
    genre = CRIMGenrePersonSummarySerializer(read_only=True)

    class Meta:
        model = CRIMMass
        fields = (
            'url',
            'title',
            'genre',
        )


class CRIMPiecePersonSummarySerializer(serializers.HyperlinkedModelSerializer):
    genre = CRIMGenrePersonSummarySerializer(read_only=True)

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'title',
            'genre',
        )


class CRIMTreatisePersonSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMTreatise
        fields = (
            'url',
            'title',
        )


class CRIMSourcePersonSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMSource
        fields = (
            'url',
            'title',
        )


class CRIMRolePersonSummarySerializer(serializers.HyperlinkedModelSerializer):
    mass = CRIMMassPersonSummarySerializer(read_only=True)
    piece = CRIMPiecePersonSummarySerializer(read_only=True)
    treatise = CRIMTreatisePersonSummarySerializer(read_only=True)
    source = CRIMSourcePersonSummarySerializer(read_only=True)
    role_type = CRIMRoleTypePersonSummarySerializer(read_only=True)

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


class CRIMPersonSerializer(serializers.HyperlinkedModelSerializer):
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

    unique_roles = serializers.SerializerMethodField()

    roles = CRIMRolePersonSummarySerializer(many=True, read_only=True)

    class Meta:
        model = CRIMPerson
        fields = (
            'url',
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
