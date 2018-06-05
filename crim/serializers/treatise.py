from crim.models.document import CRIMSource
from crim.models.person import CRIMPerson
from crim.models.role import CRIMRoleType, CRIMRole
from crim.models.document import CRIMTreatise
from rest_framework import serializers


class CRIMRoleTypeTreatiseSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimroletype-detail-data', lookup_field='role_type_id')

    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'role_type_id',
            'name',
        )


class CRIMPersonTreatiseSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimperson-detail-data', lookup_field='person_id')

    class Meta:
        model = CRIMPerson
        fields = (
            'url',
            'name',
        )


class CRIMRoleTreatiseSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrole-detail-data', lookup_field='pk')
    person = CRIMPersonTreatiseSerializer(read_only=True)
    role_type = CRIMRoleTypeTreatiseSerializer(read_only=True)

    class Meta:
        model = CRIMRole
        fields = (
            'url',
            'person',
            'role_type',
            'date',
        )


class CRIMSourceTreatiseSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='crimsource-detail-data',
        lookup_field='document_id',
    )
    roles = CRIMRoleTreatiseSerializer(
        many=True,
        read_only=True,
    )
    external_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMSource
        fields = (
            'url',
            'document_id',
            'title',
            'roles',
            'external_links',
        )

    def get_external_links(self, obj):
        return obj.external_links.split('\n')


class CRIMTreatiseListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimtreatise-detail-data', lookup_field='document_id')
    roles = CRIMRoleTreatiseSerializer(
        many=True,
        read_only=True,
        source='roles_as_treatise',
    )
    external_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMTreatise
        fields = (
            'url',
            'document_id',
            'title',
            'roles',
            'external_links',
            'remarks',
        )

    def get_external_links(self, obj):
        return obj.external_links.split('\n')


class CRIMTreatiseDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimtreatise-detail-data', lookup_field='document_id')
    roles = CRIMRoleTreatiseSerializer(
        many=True,
        read_only=True,
        source='roles_as_treatise',
    )
    sources = CRIMSourceTreatiseSerializer(
        many=True,
        read_only=True,
        source='source_contents',
    )
    external_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMTreatise
        fields = (
            'url',
            'document_id',
            'title',
            'roles',
            'sources',
            'external_links',
            'remarks',
        )

    def get_external_links(self, obj):
        return obj.external_links.split('\n')
