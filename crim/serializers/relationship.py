from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece
from crim.models.relationship import CRIMRelationship
from crim.models.observation import CRIMObservation
from rest_framework import serializers


class CRIMPersonRelationshipSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimperson-detail-data', lookup_field='person_id')

    class Meta:
        model = CRIMPerson
        fields = (
            'url',
            'name',
        )


class CRIMPieceRelationshipSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
        )


class CRIMObservationRelationshipSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimobservation-detail-data')
    piece = CRIMPieceRelationshipSerializer(read_only=True)

    class Meta:
        model = CRIMObservation
        fields = (
            'url',
            'piece',
            'ema',
        )


class CRIMRelationshipSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrelationship-detail-data')
    observer = CRIMPersonRelationshipSerializer(read_only=True)
    model_observation = CRIMObservationRelationshipSerializer(read_only=True)
    derivative_observation = CRIMObservationRelationshipSerializer(read_only=True)

    class Meta:
        model = CRIMRelationship
        fields = (
            'url',
            'observer',
            'model_observation',
            'derivative_observation',
            'rt_q',
            'rt_q_exact',
            'rt_q_monnayage',
            'rt_tm',
            'rt_tm_snd',
            'rt_tm_minv',
            'rt_tm_retrograde',
            'rt_tm_ms',
            'rt_tm_transposed',
            'rt_tm_invertible',
            'rt_tnm',
            'rt_tnm_embellished',
            'rt_tnm_reduced',
            'rt_tnm_amplified',
            'rt_tnm_truncated',
            'rt_tnm_ncs',
            'rt_tnm_ocs',
            'rt_tnm_ocst',
            'rt_tnm_nc',
            'rt_nm',
            'rt_om',
            'remarks',
            'created',
            'updated',
        )
