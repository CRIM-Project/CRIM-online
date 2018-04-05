from crim.models.document import CRIMSource
from crim.models.role import CRIMRole
from rest_framework import serializers


class CRIMRoleSourceSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMRole
        fields = (
            'url',
            'person',
            'role_type',
            'date',
        )


class CRIMSourceListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMSource
        fields = (
            'url',
            'title',
            'people',
        )


class CRIMSourceDetailSerializer(serializers.HyperlinkedModelSerializer):
    roles = CRIMRoleSourceSummarySerializer(
        many=True,
        read_only=True,
        source='roles_as_Source',
    )

    class Meta:
        model = CRIMSource
        fields = (
            'url',
            'title',
            'roles',
            'remarks',
        )
