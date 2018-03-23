from crim.models.person import CRIMPerson
from crim.models.role import CRIMRole
from rest_framework import serializers


class CRIMPersonListSerializer(serializers.HyperlinkedModelSerializer):
    def get_roles(self, obj):
        unique_roles = []
        crimroles = CRIMRole.objects.filter(person=obj)
        for crimrole in crimroles:
            role_type_name = crimrole.role_type.name
            if role_type_name not in unique_roles:
                unique_roles.append(role_type_name)
        unique_roles.sort()
        return unique_roles

    roles = serializers.SerializerMethodField()

    class Meta:
        model = CRIMPerson
        fields = '__all__'


class CRIMPersonDetailSerializer(serializers.HyperlinkedModelSerializer):
    def get_roles(self, obj):
        unique_roles = []
        crimroles = CRIMRole.objects.filter(person=obj)
        for crimrole in crimroles:
            role_type_name = crimrole.role_type.name
            if role_type_name not in unique_roles:
                unique_roles.append(role_type_name)
        unique_roles.sort()
        return unique_roles

    roles = serializers.SerializerMethodField()

    class Meta:
        model = CRIMPerson
        fields = '__all__'
