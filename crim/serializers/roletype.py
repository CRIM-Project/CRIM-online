from crim.models.role import CRIMRoleType
from rest_framework import serializers


class CRIMRoleTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMRoleType
        fields = '__all__'
