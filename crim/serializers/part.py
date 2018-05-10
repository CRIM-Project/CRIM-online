from crim.models.part import CRIMPart
from crim.models.piece import CRIMPiece
from rest_framework import serializers


class CRIMPiecePartSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'title',
        )


class CRIMPartSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpart-detail-data', lookup_field='part_id')
    piece = CRIMPiecePartSerializer(read_only=True)

    class Meta:
        model = CRIMPart
        fields = (
            'url',
            'piece',
            'order',
            'name',
            'remarks',
        )
