from crim.models.document import CRIMSource
from crim.models.genre import CRIMGenre
from crim.models.mass import CRIMMass
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece
from crim.models.role import CRIMRoleType, CRIMRole
from crim.models.voice import CRIMVoice
from crim.serializers.piece import CRIMPieceSummarySerializer
from rest_framework import serializers


class CRIMRoleTypeMassSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimroletype-detail-data', lookup_field='role_type_id')

    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'role_type_id',
            'name',
        )


class CRIMGenreMassSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimgenre-detail-data', lookup_field='genre_id')

    class Meta:
        model = CRIMGenre
        fields = (
            'url',
            'name',
        )


class CRIMPersonMassSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimperson-detail-data', lookup_field='person_id')

    class Meta:
        model = CRIMPerson
        fields = (
            'url',
            'name',
        )


class CRIMRoleMassSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrole-detail-data', lookup_field='id')
    person = CRIMPersonMassSerializer(read_only=True)
    role_type = CRIMRoleTypeMassSerializer(read_only=True)

    class Meta:
        model = CRIMRole
        fields = (
            'url',
            'person',
            'role_type',
            'date',
        )


class CRIMVoiceMassSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimvoice-detail-data', lookup_field='voice_id')

    class Meta:
        model = CRIMVoice
        fields = (
            'url',
        )


class CRIMPieceMassSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')
    pdf_links = serializers.SerializerMethodField()
    mei_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'pdf_links',
            'mei_links',
        )

    def get_pdf_links(self, obj):
        return obj.pdf_links.split('\n') if obj.pdf_links else []

    def get_mei_links(self, obj):
        return obj.mei_links.split('\n') if obj.mei_links else []


class CRIMSourceMassSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='crimsource-detail-data',
        lookup_field='document_id',
    )
    publisher = CRIMPersonMassSerializer(read_only=True)
    external_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMSource
        fields = (
            'url',
            'document_id',
            'title',
            'publisher',
            'date',
            'external_links',
        )

    def get_external_links(self, obj):
        return obj.external_links.split('\n') if obj.external_links else []


class CRIMMassListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimmass-detail-data', lookup_field='mass_id')
    composer = CRIMPersonMassSerializer(read_only=True)

    class Meta:
        model = CRIMMass
        fields = (
            'url',
            'mass_id',
            'title',
            'composer',
            'date',
            'date_sort',
            'min_number_of_voices',
            'max_number_of_voices',
            'remarks',
        )


class CRIMMassDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimmass-detail-data', lookup_field='mass_id')
    genre = CRIMGenreMassSerializer(read_only=True)
    roles = CRIMRoleMassSerializer(
        many=True,
        read_only=True,
        source='roles_as_mass',
    )
    movements = CRIMPieceMassSerializer(
        many=True,
        read_only=True,
    )
    sources = CRIMSourceMassSerializer(
        many=True,
        read_only=True,
    )
    models = CRIMPieceSummarySerializer(
        many=True,
        read_only=True,
    )
    derivatives = CRIMPieceSummarySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = CRIMMass
        fields = (
            'url',
            'mass_id',
            'title',
            'genre',
            'roles',
            'movements',
            'sources',
            'models',
            'derivatives',
            'remarks',
        )
