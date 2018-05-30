from crim.models.genre import CRIMGenre
from crim.models.mass import CRIMMass
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece
from crim.models.role import CRIMRole, CRIMRoleType
from rest_framework import serializers


class CRIMRoleTypeGenreSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimroletype-detail-data', lookup_field='role_type_id')

    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'name',
        )


class CRIMPersonGenreSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimperson-detail-data', lookup_field='person_id')

    class Meta:
        model = CRIMPerson
        fields = (
            'url',
            'name',
        )


class CRIMRoleGenreSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrole-detail-data', lookup_field='pk')
    person = CRIMPersonGenreSerializer(read_only=True)
    role_type = CRIMRoleTypeGenreSerializer(read_only=True)

    class Meta:
        model = CRIMRole
        fields = (
            'url',
            'person',
            'role_type',
            'date',
            'remarks',
        )


class CRIMMassGenreSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='crimmass-detail-data',
        lookup_field='mass_id',
    )
    roles = CRIMRoleGenreSerializer(
        many=True,
        read_only=True,
        source='roles_as_mass',
    )

    class Meta:
        model = CRIMMass
        fields = (
            'url',
            'mass_id',
            'title',
            'roles',
        )


class CRIMPieceGenreSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')
    roles = CRIMRoleGenreSerializer(
        many=True,
        read_only=True,
        source='roles_as_piece',
    )
    mass = CRIMMassGenreSerializer(read_only=True)
    pdf_links = serializers.SerializerMethodField()
    mei_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
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


class CRIMGenreListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimgenre-detail-data', lookup_field='genre_id')
    number_of_pieces = serializers.SerializerMethodField()

    class Meta:
        model = CRIMGenre
        fields = (
            'url',
            'name',
            'remarks',
            'number_of_pieces',
        )

    def get_number_of_pieces(self, obj):
        pieces = CRIMPiece.objects.filter(genre=obj)
        return len(pieces)


class CRIMGenreDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimgenre-detail-data', lookup_field='genre_id')
    pieces = CRIMPieceGenreSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = CRIMGenre
        fields = (
            'url',
            'name',
            'remarks',
            'pieces',
        )
