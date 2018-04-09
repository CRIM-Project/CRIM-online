from crim.models.person import CRIMPerson
from crim.models.mass import CRIMMass
from crim.models.piece import CRIMPiece
from crim.models.role import CRIMRoleType, CRIMRole
from crim.models.document import CRIMTreatise, CRIMSource
from rest_framework import serializers


class CRIMRoleTypeSourceSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'name',
        )


class CRIMPersonSourceSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CRIMPerson
        fields = (
            'url',
            'name',
        )


class CRIMRoleSourceSummarySerializer(serializers.HyperlinkedModelSerializer):
    person = CRIMPersonSourceSummarySerializer(read_only=True)
    role_type = CRIMRoleTypeSourceSummarySerializer(read_only=True)

    class Meta:
        model = CRIMRole
        fields = (
            'url',
            'person',
            'role_type',
            'date',
        )


class CRIMMassSourceSummarySerializer(serializers.HyperlinkedModelSerializer):
    roles = CRIMRoleSourceSummarySerializer(
        many=True,
        read_only=True,
        source='roles_as_mass',
    )

    class Meta:
        model = CRIMMass
        fields = (
            'url',
            'mass_id',
            'title',
            'genre',
            'roles',
            'remarks',
        )


class CRIMPieceSourceSummarySerializer(serializers.HyperlinkedModelSerializer):
    roles = CRIMRoleSourceSummarySerializer(
        many=True,
        read_only=True,
        source='roles_as_piece',
    )

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'title',
            'genre',
            'roles',
            'remarks',
        )


class CRIMTreatiseSourceSummarySerializer(serializers.HyperlinkedModelSerializer):
    roles = CRIMRoleSourceSummarySerializer(
        many=True,
        read_only=True,
        source='roles_as_treatise',
    )

    class Meta:
        model = CRIMTreatise
        fields = (
            'url',
            'document_id',
            'title',
            'roles',
            'remarks',
        )


class CRIMSourceSourceSummarySerializer(serializers.HyperlinkedModelSerializer):
    roles = CRIMRoleSourceSummarySerializer(
        many=True,
        read_only=True,
        source='roles_as_source',
    )

    class Meta:
        model = CRIMSource
        fields = (
            'url',
            'document_id',
            'title',
            'roles',
            'remarks',
        )


class CRIMSourceListSerializer(serializers.HyperlinkedModelSerializer):
    roles = CRIMRoleSourceSummarySerializer(
        many=True,
        read_only=True,
        source='roles_as_source',
    )

    class Meta:
        model = CRIMSource
        fields = (
            'url',
            'document_id',
            'title',
            'roles',
            'remarks',
        )


class CRIMSourceDetailSerializer(serializers.HyperlinkedModelSerializer):
    mass_contents = CRIMMassSourceSummarySerializer(
        many=True,
        read_only=True,
    )
    piece_contents = CRIMPieceSourceSummarySerializer(
        many=True,
        read_only=True,
    )
    treatise_contents = CRIMTreatiseSourceSummarySerializer(
        many=True,
        read_only=True,
    )
    source_contents = CRIMSourceSourceSummarySerializer(
        many=True,
        read_only=True,
    )
    roles = CRIMRoleSourceSummarySerializer(
        many=True,
        read_only=True,
        source='roles_as_source',
    )

    class Meta:
        model = CRIMSource
        fields = (
            'url',
            'document_id',
            'title',
            'roles',
            'pdf_link',
            'mass_contents',
            'piece_contents',
            'treatise_contents',
            'source_contents',
            'remarks',
        )
