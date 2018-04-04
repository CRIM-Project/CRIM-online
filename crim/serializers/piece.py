from crim.models.piece import CRIMPiece
from crim.models.role import CRIMRole
from crim.serializers.role import CRIMRoleSerializer
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
    roles = serializers.HyperlinkedRelatedField(
        view_name='crimrole-detail',
        queryset=CRIMRole.objects.all(),
        many=True,
        source='roles_as_piece',
    )

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
