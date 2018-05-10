from crim.models.genre import CRIMGenre
from rest_framework import serializers


class CRIMGenreSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimgenre-detail-data', lookup_field='genre_id')

    class Meta:
        model = CRIMGenre
        fields = (
            'url',
            'name',
            'remarks',
        )
