from crim.models.genre import CRIMGenre
from crim.models.mass import CRIMMass
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece
from crim.models.role import CRIMRoleType, CRIMRole
from rest_framework import serializers


class CRIMRoleTypePieceSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimroletype-detail', lookup_field='role_type_id')

    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'name',
        )


class CRIMGenrePieceSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimgenre-detail', lookup_field='genre_id')

    class Meta:
        model = CRIMGenre
        fields = (
            'url',
            'name',
        )


class CRIMPersonPieceSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimperson-detail', lookup_field='person_id')

    class Meta:
        model = CRIMPerson
        fields = (
            'url',
            'name',
        )


class CRIMRolePieceSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrole-detail', lookup_field='pk')
    person = CRIMPersonPieceSummarySerializer(read_only=True)
    role_type = CRIMRoleTypePieceSummarySerializer(read_only=True)

    class Meta:
        model = CRIMRole
        fields = (
            'url',
            'person',
            'role_type',
            'date',
            'remarks',
        )


class CRIMPieceListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail', lookup_field='piece_id')
    roles = CRIMRolePieceSummarySerializer(
        many=True,
        read_only=True,
        source='roles_as_piece',
    )
    genre = CRIMGenrePieceSummarySerializer(read_only=True)
#     unique_roles = serializers.SerializerMethodField()

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'genre',
            'roles',
            'remarks',
        )


class CRIMPieceDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail', lookup_field='piece_id')
    roles = CRIMRolePieceSummarySerializer(
        many=True,
        read_only=True,
        source='roles_as_piece',
    )
    genre = CRIMGenrePieceSummarySerializer(read_only=True)

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'genre',
            'roles',
            'pdf_link',
            'mei_link',
            'remarks',
        )
