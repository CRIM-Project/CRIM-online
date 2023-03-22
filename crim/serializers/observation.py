from crim.models.definition import CRIMDefinition
from crim.models.observation import CRIMObservation, CJObservation
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece
from crim.models.relationship import CRIMRelationship, CJRelationship
from crim.models.role import CRIMRole, CRIMRoleType
from rest_framework import serializers


class CRIMDefinitionObservationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimdefinition-detail-data', lookup_field='id')

    class Meta:
        model = CRIMDefinition
        fields = (
            'url',
            'id',
            'observation_definition',
        )


class CRIMPersonObservationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimperson-detail-data', lookup_field='person_id')

    class Meta:
        model = CRIMPerson
        fields = (
            'url',
            'name',
            'id',
        )


class CRIMRoleTypeObservationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimroletype-detail-data', lookup_field='role_type_id')

    class Meta:
        model = CRIMRoleType
        fields = (
            'url',
            'role_type_id',
            'name',
        )


class CRIMRoleObservationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrole-detail-data', lookup_field='id')
    person = CRIMPersonObservationSerializer(read_only=True)
    role_type = CRIMRoleTypeObservationSerializer(read_only=True)

    class Meta:
        model = CRIMRole
        fields = (
            'url',
            'person',
            'role_type',
        )


class CRIMPieceObservationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')
    roles = CRIMRoleObservationSerializer(
        many=True,
        read_only=True,
        source='roles_as_piece',
    )
    pdf_links = serializers.SerializerMethodField()
    mei_links = serializers.SerializerMethodField()

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'full_title',
            'roles',
            'mei_links',
            'pdf_links',
        )

    def get_pdf_links(self, obj):
        return obj.pdf_links.split('\n') if obj.pdf_links else []

    def get_mei_links(self, obj):
        return obj.mei_links.split('\n') if obj.mei_links else []


class CRIMPieceObservationSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimpiece-detail-data', lookup_field='piece_id')

    class Meta:
        model = CRIMPiece
        fields = (
            'url',
            'piece_id',
            'full_title',
            'mass',
        )


# Deprecated class
class CRIMObservationSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimobservation-detail-data', lookup_field='id')
    piece = CRIMPieceObservationSummarySerializer(read_only=True)

    class Meta:
        model = CRIMObservation
        fields = (
            'url',
            'id',
            'piece',
        )

class CJObservationSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='cjobservation-detail-data', lookup_field='id')
    piece = CRIMPieceObservationSummarySerializer(read_only=True)

    class Meta:
        model = CJObservation
        fields = (
            'url',
            'id',
            'piece',
        )


# Deprecated class
class CRIMRelationshipObservationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimrelationship-detail-data', lookup_field='id')
    observer = CRIMPersonObservationSerializer(read_only=True)
    model_observation = CRIMObservationSummarySerializer(read_only=True)
    derivative_observation = CRIMObservationSummarySerializer(read_only=True)

    class Meta:
        model = CRIMRelationship
        fields = (
            'url',
            'id',
            'observer',
            'model_observation',
            'derivative_observation',
            'relationship_type',
        )

class CJRelationshipObservationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='cjrelationship-detail-data', lookup_field='id')
    observer = CRIMPersonObservationSerializer(read_only=True)
    model_observation = CJObservationSummarySerializer(read_only=True)
    derivative_observation = CJObservationSummarySerializer(read_only=True)

    class Meta:
        model = CJRelationship
        fields = (
            'url',
            'id',
            'observer',
            'model_observation',
            'derivative_observation',
            'relationship_type',
        )


# Deprecated class
class CRIMObservationDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimobservation-detail-data', lookup_field='id')
    observer = CRIMPersonObservationSerializer(read_only=True)
    piece = CRIMPieceObservationSerializer(read_only=True)
    relationships_as_model = CRIMRelationshipObservationSerializer(
        many=True,
        read_only=True,
        source='observations_as_model',
    )
    relationships_as_derivative = CRIMRelationshipObservationSerializer(
        many=True,
        read_only=True,
        source='observations_as_derivative',
    )

    class Meta:
        model = CRIMObservation
        fields = (
            'url',
            'id',
            'observer',
            'piece',
            'ema',
            'musical_type',
            'relationships_as_model',
            'relationships_as_derivative',
            'mt_cf',
            'mt_cf_voices',
            'mt_cf_dur',
            'mt_cf_mel',
            'mt_sog',
            'mt_sog_voices',
            'mt_sog_dur',
            'mt_sog_mel',
            'mt_sog_ostinato',
            'mt_sog_periodic',
            'mt_csog',
            'mt_csog_voices',
            'mt_csog_dur',
            'mt_csog_mel',
            'mt_cd',
            'mt_cd_voices',
            'mt_fg',
            'mt_fg_voices',
            'mt_fg_int',
            'mt_fg_tint',
            'mt_fg_periodic',
            'mt_fg_strict',
            'mt_fg_flexed',
            'mt_fg_sequential',
            'mt_fg_inverted',
            'mt_fg_retrograde',
            'mt_pe',
            'mt_pe_voices',
            'mt_pe_int',
            'mt_pe_tint',
            'mt_pe_strict',
            'mt_pe_flexed',
            'mt_pe_flt',
            'mt_pe_sequential',
            'mt_pe_added',
            'mt_pe_invertible',
            'mt_id',
            'mt_id_voices',
            'mt_id_int',
            'mt_id_tint',
            'mt_id_strict',
            'mt_id_flexed',
            'mt_id_flt',
            'mt_id_invertible',
            'mt_nid',
            'mt_nid_voices',
            'mt_nid_int',
            'mt_nid_tint',
            'mt_nid_strict',
            'mt_nid_flexed',
            'mt_nid_flt',
            'mt_nid_sequential',
            'mt_nid_invertible',
            'mt_hr',
            'mt_hr_voices',
            'mt_hr_simple',
            'mt_hr_staggered',
            'mt_hr_sequential',
            'mt_hr_fauxbourdon',
            'mt_cad',
            'mt_cad_cantizans',
            'mt_cad_tenorizans',
            'mt_cad_type',
            'mt_cad_tone',
            'mt_cad_dtv',
            'mt_cad_dti',
            'mt_int',
            'mt_int_voices',
            'mt_int_p6',
            'mt_int_p3',
            'mt_int_c35',
            'mt_int_c83',
            'mt_int_c65',
            'mt_fp',
            'mt_fp_ir',
            'mt_fp_range',
            'mt_fp_comment',
            'remarks',
            'created',
            'updated',
            'curated',
        )

class CJObservationDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='cjobservation-detail-data', lookup_field='id')
    observer = CRIMPersonObservationSerializer(read_only=True)
    piece = CRIMPieceObservationSerializer(read_only=True)
    relationships_as_model = CJRelationshipObservationSerializer(
        many=True,
        read_only=True,
        source='observations_as_model',
    )
    relationships_as_derivative = CJRelationshipObservationSerializer(
        many=True,
        read_only=True,
        source='observations_as_derivative',
    )
    definition = CRIMDefinitionObservationSerializer(read_only=True)
    details = serializers.JSONField()

    class Meta:
        model = CJObservation
        fields = (
            'url',
            'id',
            'observer',
            'piece',
            'ema',
            'musical_type',
            'relationships_as_model',
            'relationships_as_derivative',
            'definition',
            'details',
            'remarks',
            'created',
            'updated',
            'curated',
        )


# Deprecated class
class CRIMObservationListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimobservation-detail-data', lookup_field='id')
    observer = CRIMPersonObservationSerializer(read_only=True)
    piece = CRIMPieceObservationSummarySerializer(read_only=True)

    class Meta:
        model = CRIMObservation
        fields = (
            'url',
            'id',
            'observer',
            'piece',
            'ema',
            'musical_type',
            'mt_cf',
            'mt_cf_voices',
            'mt_cf_dur',
            'mt_cf_mel',
            'mt_sog',
            'mt_sog_voices',
            'mt_sog_dur',
            'mt_sog_mel',
            'mt_sog_ostinato',
            'mt_sog_periodic',
            'mt_csog',
            'mt_csog_voices',
            'mt_csog_dur',
            'mt_csog_mel',
            'mt_cd',
            'mt_cd_voices',
            'mt_fg',
            'mt_fg_voices',
            'mt_fg_int',
            'mt_fg_tint',
            'mt_fg_periodic',
            'mt_fg_strict',
            'mt_fg_flexed',
            'mt_fg_sequential',
            'mt_fg_inverted',
            'mt_fg_retrograde',
            'mt_pe',
            'mt_pe_voices',
            'mt_pe_int',
            'mt_pe_tint',
            'mt_pe_strict',
            'mt_pe_flexed',
            'mt_pe_flt',
            'mt_pe_sequential',
            'mt_pe_added',
            'mt_pe_invertible',
            'mt_id',
            'mt_id_voices',
            'mt_id_int',
            'mt_id_tint',
            'mt_id_strict',
            'mt_id_flexed',
            'mt_id_flt',
            'mt_id_invertible',
            'mt_nid',
            'mt_nid_voices',
            'mt_nid_int',
            'mt_nid_tint',
            'mt_nid_strict',
            'mt_nid_flexed',
            'mt_nid_flt',
            'mt_nid_sequential',
            'mt_nid_invertible',
            'mt_hr',
            'mt_hr_voices',
            'mt_hr_simple',
            'mt_hr_staggered',
            'mt_hr_sequential',
            'mt_hr_fauxbourdon',
            'mt_cad',
            'mt_cad_cantizans',
            'mt_cad_tenorizans',
            'mt_cad_type',
            'mt_cad_tone',
            'mt_cad_dtv',
            'mt_cad_dti',
            'mt_int',
            'mt_int_voices',
            'mt_int_p6',
            'mt_int_p3',
            'mt_int_c35',
            'mt_int_c83',
            'mt_int_c65',
            'mt_fp',
            'mt_fp_ir',
            'mt_fp_range',
            'mt_fp_comment',
            'remarks',
            'created',
            'updated',
            'curated',
        )

class CJObservationListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='cjobservation-detail-data', lookup_field='id')
    observer = CRIMPersonObservationSerializer(read_only=True)
    piece = CRIMPieceObservationSummarySerializer(read_only=True)
    definition = CRIMDefinitionObservationSerializer(read_only=True)

    class Meta:
        model = CJObservation
        fields = (
            'url',
            'id',
            'observer',
            'piece',
            'ema',
            'musical_type',
            'details',
            'definition',
            'remarks',
            'created',
            'updated',
            'curated',
        )


# Deprecated class
class CRIMObservationBriefSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='crimobservation-detail-data', lookup_field='id')
    observer = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
    piece = serializers.PrimaryKeyRelatedField(many=False,read_only=True)

    class Meta:
        model = CRIMObservation
        fields = (
            'url',
            'id',
            'observer',
            'musical_type',
            'piece',
            'ema',
        )

class CJObservationBriefSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='cjobservation-detail-data', lookup_field='id')
    observer = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
    piece = serializers.PrimaryKeyRelatedField(many=False,read_only=True)

    class Meta:
        model = CJObservation
        fields = (
            'url',
            'id',
            'observer',
            'musical_type',
            'piece',
            'ema',
        )
