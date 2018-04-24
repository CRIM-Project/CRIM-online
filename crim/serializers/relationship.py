from crim.models.relationship import CRIMRelationship
from rest_framework import serializers


class CRIMRelationshipSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrelationship-detail', lookup_field='relationship_id')

    class Meta:
        model = CRIMRelationship
        fields = (
            'url',
            'observer',
            'model_observation',
            'derivative_observation',
            'reverse_direction',
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
