from crim.models.person import CRIMPerson
from crim.models.role import CRIMRoleType, CRIMRole
from crim.models.document import CRIMTreatise
from rest_framework import serializers


class CRIMRoleTypeTreatiseSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimroletype-detail', lookup_field='role_type_id')

    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'name',
        )


class CRIMPersonTreatiseSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimperson-detail', lookup_field='person_id')

    class Meta:
        model = CRIMPerson
        fields = (
            'url',
            'name',
        )


class CRIMRoleTreatiseSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrole-detail', lookup_field='pk')
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
    url = serializers.HyperlinkedIdentityField(view_name='crimtreatise-detail', lookup_field='document_id')
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
    url = serializers.HyperlinkedIdentityField(view_name='crimtreatise-detail', lookup_field='document_id')
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
