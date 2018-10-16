from rest_framework import serializers

from crim.models.person import CRIMPerson
from crim.models.user import CRIMUserProfile


class CRIMPersonUserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimperson-detail-data', lookup_field='person_id')

    class Meta:
        model = CRIMPerson
        fields = (
            'url',
        )


class CRIMUserProfileDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimuserprofile-detail-data', lookup_field='username')
    person = CRIMPersonUserSerializer(read_only=True)

    class Meta:
        model = CRIMUserProfile
        fields = [
            'url',
            'username',
            'name',
            'name_sort',
            'person',
        ]
