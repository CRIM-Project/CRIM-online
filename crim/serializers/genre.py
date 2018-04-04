from crim.models.piece import CRIMGenre
from rest_framework import serializers


class CRIMGenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMGenre
        fields = '__all__'
