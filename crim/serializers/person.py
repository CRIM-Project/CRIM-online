from crim.models.person import CRIMPerson
from crim.models.role import CRIMRole
from crim.serializers.role import CRIMRoleSerializer
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

    roles = CRIMRoleSerializer(many=True, read_only=True)
#     roles = serializers.HyperlinkedRelatedField(
#         view_name='crimrole-detail',
#         queryset=CRIMRole.objects.all(),
#         many=True,
#     )

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
