from crim.models.phrase import CRIMPhrase
from rest_framework import serializers


class CRIMPhraseSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimphrase-detail', lookup_field='phrase_id')

    class Meta:
        model = CRIMPhrase
        fields = (
            'url',
            'piece',
            'part',
            'number',
            'text',
            'remarks',
        )
