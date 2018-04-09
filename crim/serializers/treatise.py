from crim.models.person import CRIMPerson
from crim.models.role import CRIMRoleType, CRIMRole
from crim.models.document import CRIMTreatise
from rest_framework import serializers


class CRIMRoleTypeTreatiseSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'name',
        )


class CRIMPersonTreatiseSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMPerson
        fields = (
            'url',
            'name',
        )


class CRIMRoleTreatiseSummarySerializer(serializers.HyperlinkedModelSerializer):
    person = CRIMPersonTreatiseSummarySerializer(read_only=True)
    role_type = CRIMRoleTypeTreatiseSummarySerializer(read_only=True)

    class Meta:
        model = CRIMRole
        fields = (
            'url',
            'person',
            'role_type',
            'date',
        )


class CRIMTreatiseListSerializer(serializers.HyperlinkedModelSerializer):
    roles = CRIMRoleTreatiseSummarySerializer(
        many=True,
        read_only=True,
        source='roles_as_treatise',
    )

    class Meta:
        model = CRIMTreatise
        fields = (
            'url',
            'document_id',
            'title',
            'roles',
            'remarks',
        )


class CRIMTreatiseDetailSerializer(serializers.HyperlinkedModelSerializer):
    roles = CRIMRoleTreatiseSummarySerializer(
        many=True,
        read_only=True,
        source='roles_as_treatise',
    )

    class Meta:
        model = CRIMTreatise
        fields = (
            'url',
            'document_id',
            'title',
            'roles',
            'pdf_link',
            'remarks',
        )
