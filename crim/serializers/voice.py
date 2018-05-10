from crim.models.voice import CRIMVoice
from rest_framework import serializers


class CRIMVoiceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimvoice-detail', lookup_field='voice_id')

    class Meta:
        model = CRIMVoice
        fields = (
            'url',
            'piece',
            'name',
            'order',
            'supplied',
            'clef',
            'remarks',
        )
