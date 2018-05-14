from crim.models.part import CRIMPart
from crim.models.phrase import CRIMPhrase
from crim.models.piece import CRIMPiece
from rest_framework import serializers


class CRIMPiecePhraseSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'title',
        )


class CRIMPartPhraseSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpart-detail-data', lookup_field='part_id')

    class Meta:
        model = CRIMPart
        fields = (
            'url',
            'name',
        )


class CRIMPhraseSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimphrase-detail-data', lookup_field='phrase_id')
    part = CRIMPartPhraseSerializer(read_only=True)
    piece = CRIMPiecePhraseSerializer(read_only=True)

    class Meta:
        model = CRIMPhrase
        fields = (
            'url',
            'piece',
            'part',
            'number',
            'start_measure',
            'stop_measure',
            'text',
            'translation',
            'remarks',
        )
