from crim.models.document import CRIMTreatise
from crim.models.role import CRIMRole
from rest_framework import serializers


class CRIMRoleTreatiseSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMRole
        fields = (
            'url',
            'person',
            'role_type',
            'date',
        )


class CRIMTreatiseListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMTreatise
        fields = (
            'url',
            'title',
            'people',
        )


class CRIMTreatiseDetailSerializer(serializers.HyperlinkedModelSerializer):
    roles = CRIMRoleTreatiseSummarySerializer(
        many=True,
        read_only=True,
        source='roles_as_Treatise',
    )

    class Meta:
        model = CRIMTreatise
        fields = (
            'url',
            'title',
            'roles',
            'remarks',
        )
