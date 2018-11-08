from crim.models.comment import CRIMComment
from crim.models.mass import CRIMMass
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece
from crim.models.user import CRIMUserProfile

from django.contrib.auth.models import User
from rest_framework import serializers


class CRIMPersonCommentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimperson-detail-data', lookup_field='person_id')

    class Meta:
        model = CRIMPerson
        fields = (
            'url',
        )


class CRIMUserProfileCommentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimuserprofile-detail-data', lookup_field='username')
    person = CRIMPersonCommentSerializer(read_only=True)

    class Meta:
        model = CRIMUserProfile
        fields = (
            'url',
            'person',
            'name',
            'name_sort',
        )


class CRIMMassCommentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimmass-detail-data', lookup_field='mass_id')

    class Meta:
        model = CRIMMass
        fields = (
            'url',
            'mass_id',
            'title',
        )


class CRIMPieceCommentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')
    mass = CRIMMassCommentSerializer(read_only=True)

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'mass',
            'title',
        )


class CRIMCommentListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimcomment-detail-data', lookup_field='comment_id')
    author = CRIMUserProfileCommentSerializer(read_only=True)
    piece = CRIMPieceCommentSerializer(read_only=True)
    # TODO: Use generic foreign key so that comments can connect to pieces, masses, sources, and
    #       other types of object.

    class Meta:
        model = CRIMComment
        fields = (
            'url',
            'author',
            'piece',
            'text',
            'created',
            'updated',
            'edited',
            'alive',
        )


class CRIMCommentDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimcomment-detail-data', lookup_field='comment_id')
    author = CRIMUserProfileCommentSerializer(read_only=True)
    piece = serializers.PrimaryKeyRelatedField(read_only=False, queryset=CRIMPiece.objects.all())
    # TODO: Use generic foreign key so that comments can connect to pieces, masses, sources, and
    #       other types of object.
    # TODO: Use `piece_id` instead of primary key, if possible, for security and clarity.

    class Meta:
        model = CRIMComment
        fields = (
            'url',
            'author',
            'piece',
            'text',
            'created',
            'updated',
            'edited',
            'alive',
        )

    def to_representation(self, instance):
        self.fields['piece_read'] = CRIMPieceCommentSerializer(read_only=True)
        return super().to_representation(instance)


class CRIMCommentDetailDataSerializer(CRIMCommentDetailSerializer):
    class Meta:
        model = CRIMComment
        fields = (
            'url',
            'author',
            'piece',
            'text',
            'created',
            'updated',
            'edited',
        )
