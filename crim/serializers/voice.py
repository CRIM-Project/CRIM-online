from crim.models.piece import CRIMPiece
from crim.models.voice import CRIMVoice
from rest_framework import serializers


class CRIMPieceVoiceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'title',
        )


class CRIMVoiceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimvoice-detail-data', lookup_field='voice_id')
    piece = CRIMPieceVoiceSerializer(read_only=True)

    class Meta:
        model = CRIMVoice
        fields = (
            'url',
            'piece',
            'order',
            'name',
            'supplied',
            'clef',
            'remarks',
        )
