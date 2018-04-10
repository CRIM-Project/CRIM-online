from crim.models.genre import CRIMGenre
from rest_framework import serializers


class CRIMGenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMGenre
        fields = (
            'url',
            'name',
            'remarks',
        )
