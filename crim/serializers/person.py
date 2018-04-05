from crim.models.document import CRIMTreatise, CRIMSource
from crim.models.genre import CRIMGenre
from crim.models.mass import CRIMMass
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece
from crim.models.role import CRIMRoleType, CRIMRole
from rest_framework import serializers


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
