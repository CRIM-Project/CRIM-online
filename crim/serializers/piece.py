from crim.models.genre import CRIMGenre
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece
from crim.models.role import CRIMRoleType, CRIMRole
from rest_framework import serializers


class CRIMPieceListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'title',
            'genre',
            'people',
        )


class CRIMPieceDetailSerializer(serializers.HyperlinkedModelSerializer):
    roles = CRIMRolePieceSummarySerializer(many=True, read_only=True, source='roles_as_piece')

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'title',
            'genre',
            'roles',
            'pdf_link',
            'mei_link',
            'remarks',
        )
