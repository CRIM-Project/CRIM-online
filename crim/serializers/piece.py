from crim.models.document import CRIMSource
from crim.models.genre import CRIMGenre
from crim.models.mass import CRIMMass
from crim.models.observation import CJObservation
from crim.models.part import CRIMPart
from crim.models.person import CRIMPerson
from crim.models.phrase import CRIMPhrase
from crim.models.piece import CRIMPiece
from crim.models.relationship import CJRelationship
from crim.models.role import CRIMRoleType, CRIMRole
from crim.models.user import CRIMUserProfile
from crim.models.voice import CRIMVoice
from rest_framework import serializers
from crim.serializers.observation import CJObservationListSerializer
from crim.serializers.relationship import CJRelationshipListSerializer


class CRIMRoleTypePieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimroletype-detail-data', lookup_field='role_type_id')

    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'role_type_id',
            'name',
        )


class CRIMGenrePieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimgenre-detail-data', lookup_field='genre_id')

    class Meta:
        model = CRIMGenre
        fields = (
            'url',
            'name',
        )


class CRIMPersonPieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimperson-detail-data', lookup_field='person_id')

    class Meta:
        model = CRIMPerson
        fields = (
            'url',
            'name',
        )


class CRIMUserPieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimuserprofile-detail-data', lookup_field='username')
    person = CRIMPersonPieceSerializer()

    class Meta:
        model = CRIMUserProfile
        fields = (
            'url',
            'username',
            'person',
            'name',
        )


class CRIMRolePieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrole-detail-data', lookup_field='id')
    person = CRIMPersonPieceSerializer(read_only=True)
    role_type = CRIMRoleTypePieceSerializer(read_only=True)

    class Meta:
        model = CRIMRole
        fields = (
            'url',
            'person',
            'role_type',
            'date',
            'remarks',
        )


class CRIMMassMovementPieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='crimpiece-detail-data',
        lookup_field='piece_id',
    )
    pdf_links = serializers.SerializerMethodField()
    mei_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'full_title',
            'pdf_links',
            'mei_links',
        )

    def get_pdf_links(self, obj):
        return obj.pdf_links.split('\n')

    def get_mei_links(self, obj):
        return obj.mei_links.split('\n')


class CRIMMassPieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='crimmass-detail-data',
        lookup_field='mass_id',
    )
    roles = CRIMRolePieceSerializer(
        many=True,
        read_only=True,
        source='roles_as_mass',
    )
    movements = CRIMMassMovementPieceSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = CRIMMass
        fields = (
            'url',
            'mass_id',
            'title',
            'roles',
            'movements',
        )


class CRIMMassSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='crimmass-detail-data',
        lookup_field='mass_id',
    )
    composer = CRIMPersonPieceSerializer(read_only=True)
    genre = CRIMGenrePieceSerializer(read_only=True)

    class Meta:
        model = CRIMMass
        fields = (
            'url',
            'mass_id',
            'title',
            'composer',
            'genre',
            'date',
        )


class CRIMSourcePieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='crimsource-detail-data',
        lookup_field='document_id',
    )
    publisher = CRIMPersonPieceSerializer(read_only=True)
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
        return obj.external_links.split('\n')


class CRIMPieceSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')
    mass = CRIMMassSummarySerializer(many=False,read_only=True)
    composer = CRIMPersonPieceSerializer(read_only=True)
    genre = CRIMGenrePieceSerializer(read_only=True)

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'mass',
            'composer',
            'genre',
            'date',
        )


class CJObservationPieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='cjobservation-detail-data',
        lookup_field='id',
    )
    observer = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
    piece = serializers.PrimaryKeyRelatedField(many=False,read_only=True)

    class Meta:
        model = CJObservation
        fields = (
            'url',
            'id',
            'observer',
            'piece',
            'ema',
            'musical_type',
            'definition',
            'details',
            'remarks',
            'created',
            'updated',
        )


class CJRelationshipPieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrelationship-detail-data', lookup_field='id')
    observer = CRIMPersonPieceSerializer(read_only=True)
    model_observation = CJObservationPieceSerializer(read_only=True)
    derivative_observation = CJObservationPieceSerializer(read_only=True)

    class Meta:
        model = CJRelationship
        fields = (
            'url',
            'id',
            'observer',
            'model_observation',
            'derivative_observation',
            'relationship_type',
            'musical_type',
            'definition',
            'details',
            'remarks',
            'created',
            'updated',
        )


class CRIMDiscussionPieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='forum-view-post', lookup_field='post_id')
    author = CRIMUserPieceSerializer(read_only=True)

    class Meta:
        model = CJRelationship
        fields = (
            'url',
            'id',
            'author',
            'model_observation',
            'derivative_observation',
            'remarks',
            'created',
            'updated',
        )


class CRIMPartPieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpart-detail-data', lookup_field='part_id')

    class Meta:
        model = CRIMPart
        fields = (
            'url',
            'name',
            'order',
        )


class CRIMPhrasePieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimphrase-detail-data', lookup_field='phrase_id')
    part = CRIMPartPieceSerializer(read_only=True)

    class Meta:
        model = CRIMPhrase
        fields = (
            'url',
            'part',
            'number',
            'start_measure',
            'stop_measure',
            'text',
        )


class CRIMVoicePieceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimvoice-detail-data', lookup_field='voice_id')

    class Meta:
        model = CRIMVoice
        fields = (
            'url',
            'order',
            'original_name',
            'regularized_name',
            'clef',
        )


class CRIMPieceListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')
    composer = CRIMPersonPieceSerializer(read_only=True)
    genre = CRIMGenrePieceSerializer(read_only=True)
    pdf_links = serializers.SerializerMethodField()
    mei_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'full_title',
            'genre',
            'pdf_links',
            'mei_links',
            'composer',
            'date',
            'date_sort',
            'number_of_voices',
            'remarks',
        )

    def get_pdf_links(self, obj):
        return obj.pdf_links.split('\n')

    def get_mei_links(self, obj):
        return obj.mei_links.split('\n')


class CRIMPieceDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')
    roles = CRIMRolePieceSerializer(
        many=True,
        read_only=True,
        source='roles_as_piece',
    )
    mass = CRIMMassPieceSerializer(read_only=True)
    genre = CRIMGenrePieceSerializer(read_only=True)
    phrases = CRIMPhrasePieceSerializer(
        read_only=True,
        many=True,
    )
    voices = CRIMVoicePieceSerializer(
        many=True,
        read_only=True,
    )
    sources = CRIMSourcePieceSerializer(
        many=True,
        read_only=True,
    )
    pdf_links = serializers.SerializerMethodField()
    mei_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'full_title',
            'genre',
            'mass',
            'phrases',
            'voices',
            'roles',
            'sources',
            'pdf_links',
            'mei_links',
            'remarks',
        )

    def get_pdf_links(self, obj):
        return obj.pdf_links.split('\n')

    def get_mei_links(self, obj):
        return obj.mei_links.split('\n')


class CRIMPieceScoreSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')
    roles = CRIMRolePieceSerializer(
        many=True,
        read_only=True,
        source='roles_as_piece',
    )
    mass = CRIMMassPieceSerializer(read_only=True)
    genre = CRIMGenrePieceSerializer(read_only=True)
    pdf_links = serializers.SerializerMethodField()
    mei_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'full_title',
            'genre',
            'mass',
            'roles',
            'pdf_links',
            'mei_links',
            'remarks',
        )

    def get_pdf_links(self, obj):
        return obj.pdf_links.split('\n')

    def get_mei_links(self, obj):
        return obj.mei_links.split('\n')


class CRIMPieceWithSourcesSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')
    roles = CRIMRolePieceSerializer(
        many=True,
        read_only=True,
        source='roles_as_piece',
    )
    mass = CRIMMassPieceSerializer(read_only=True)
    genre = CRIMGenrePieceSerializer(read_only=True)
    phrases = CRIMPhrasePieceSerializer(
        read_only=True,
        many=True,
    )
    voices = CRIMVoicePieceSerializer(
        many=True,
        read_only=True,
    )
    sources = CRIMSourcePieceSerializer(
        many=True,
        read_only=True,
    )
    pdf_links = serializers.SerializerMethodField()
    mei_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'full_title',
            'genre',
            'mass',
            'phrases',
            'voices',
            'roles',
            'sources',
            'pdf_links',
            'mei_links',
            'remarks',
        )

    def get_pdf_links(self, obj):
        return obj.pdf_links.split('\n')

    def get_mei_links(self, obj):
        return obj.mei_links.split('\n')


class CRIMPieceWithRelationshipsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')
    roles = CRIMRolePieceSerializer(
        many=True,
        read_only=True,
        source='roles_as_piece',
    )
    mass = CRIMMassPieceSerializer(read_only=True)
    genre = CRIMGenrePieceSerializer(read_only=True)
    models = CRIMPieceSummarySerializer(
        many=True,
        read_only=True
    )
    relationships_as_model = CJRelationshipListSerializer(many=True, read_only=True)
    derivatives = CRIMPieceSummarySerializer(
        many=True,
        read_only=True
    )
    relationships_as_derivative = CJRelationshipListSerializer(many=True, read_only=True)
    pdf_links = serializers.SerializerMethodField()
    mei_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'full_title',
            'genre',
            'mass',
            'roles',
            'models',
            'relationships_as_model',
            'derivatives',
            'relationships_as_derivative',
            'pdf_links',
            'mei_links',
            'remarks',
        )

    def get_pdf_links(self, obj):
        return obj.pdf_links.split('\n')

    def get_mei_links(self, obj):
        return obj.mei_links.split('\n')


class CRIMPieceWithObservationsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')
    roles = CRIMRolePieceSerializer(
        many=True,
        read_only=True,
        source='roles_as_piece',
    )
    mass = CRIMMassPieceSerializer(read_only=True)
    genre = CRIMGenrePieceSerializer(read_only=True)
    observations = CJObservationListSerializer(many=True, read_only=True)
    pdf_links = serializers.SerializerMethodField()
    mei_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'full_title',
            'genre',
            'mass',
            'roles',
            'observations',
            'pdf_links',
            'mei_links',
            'remarks',
        )

    def get_pdf_links(self, obj):
        return obj.pdf_links.split('\n')

    def get_mei_links(self, obj):
        return obj.mei_links.split('\n')

class CRIMPieceWithRelationshipsDataSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')
    roles = CRIMRolePieceSerializer(
        many=True,
        read_only=True,
        source='roles_as_piece',
    )
    relationships_as_model = CJRelationshipPieceSerializer(
        many=True,
        read_only=True,
    )
    relationships_as_derivative = CJRelationshipPieceSerializer(
        many=True,
        read_only=True,
    )
    mass = CRIMMassPieceSerializer(read_only=True)
    genre = CRIMGenrePieceSerializer(read_only=True)
    pdf_links = serializers.SerializerMethodField()
    mei_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'full_title',
            'genre',
            'mass',
            'roles',
            'relationships_as_model',
            'relationships_as_derivative',
            'pdf_links',
            'mei_links',
            'remarks',
        )

    def get_pdf_links(self, obj):
        return obj.pdf_links.split('\n')

    def get_mei_links(self, obj):
        return obj.mei_links.split('\n')


class CRIMPieceWithDiscussionsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')
    roles = CRIMRolePieceSerializer(
        many=True,
        read_only=True,
        source='roles_as_piece',
    )
    mass = CRIMMassPieceSerializer(read_only=True)
    genre = CRIMGenrePieceSerializer(read_only=True)
    phrases = CRIMPhrasePieceSerializer(
        read_only=True,
        many=True,
    )
    sources = CRIMSourcePieceSerializer(
        many=True,
        read_only=True,
    )
    discussions = CRIMDiscussionPieceSerializer(
        many=True,
        read_only=True,
    )
    pdf_links = serializers.SerializerMethodField()
    mei_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'full_title',
            'genre',
            'mass',
            'phrases',
            'roles',
            'sources',
            'discussions',
            'pdf_links',
            'mei_links',
            'remarks',
        )

    def get_pdf_links(self, obj):
        return obj.pdf_links.split('\n')

    def get_mei_links(self, obj):
        return obj.mei_links.split('\n')
