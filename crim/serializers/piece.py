from crim.models.genre import CRIMGenre
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece
from crim.models.role import CRIMRoleType, CRIMRole
from rest_framework import serializers


class CRIMRoleTypePieceSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'name',
        )


class CRIMGenrePieceSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMGenre
        fields = (
            'url',
            'name',
        )


class CRIMPersonPieceSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMPerson
        fields = (
            'url',
            'name',
        )


class CRIMRolePieceSummarySerializer(serializers.HyperlinkedModelSerializer):
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
