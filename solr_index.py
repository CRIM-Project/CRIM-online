#!/usr/bin/env python
import os
import sys
import solr

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crim.settings')
import django
django.setup()
from django.conf import settings

from crim.models.relationship import CRIMRelationship


if __name__ == '__main__':
    print('Using: {0}'.format(settings.SOLR_SERVER))
    solrconn = solr.SolrConnection(settings.SOLR_SERVER)

    relationships = CRIMRelationship.objects.all()
    for i, relationship in enumerate(relationships):
        # Don't index "needs review" relationships
        if not relationship.curated:
            continue

        # The suffixes are for automatic creation of the schema using
        # the correct types -- see http://yonik.com/solr-tutorial/
        d = {
            'type': 'crim_relationship',
            'id': relationship.id,
            'observer_s': relationship.observer.name,
            'observer_id_s': relationship.observer.id,
            'musical_type_s': relationship.musical_type,

            # Information about the relationship type

            'relationship_type_s': relationship.relationship_type,

            'rt_q_b': relationship.rt_q,
            'rt_q_x_b': relationship.rt_q_x,
            'rt_q_monnayage_b': relationship.rt_q_monnayage,

            'rt_tm_b': relationship.rt_tm,
            'rt_tm_snd_b': relationship.rt_tm_snd,
            'rt_tm_minv_b': relationship.rt_tm_minv,
            'rt_tm_retrograde_b': relationship.rt_tm_retrograde,
            'rt_tm_ms_b': relationship.rt_tm_ms,
            'rt_tm_transposed_b': relationship.rt_tm_transposed,
            'rt_tm_invertible_b': relationship.rt_tm_invertible,

            'rt_tnm_b': relationship.rt_tnm,
            'rt_tnm_embellished_b': relationship.rt_tnm_embellished,
            'rt_tnm_reduced_b': relationship.rt_tnm_reduced,
            'rt_tnm_amplified_b': relationship.rt_tnm_amplified,
            'rt_tnm_truncated_b': relationship.rt_tnm_truncated,
            'rt_tnm_ncs_b': relationship.rt_tnm_ncs,
            'rt_tnm_ocs_b': relationship.rt_tnm_ocs,
            'rt_tnm_ocst_b': relationship.rt_tnm_ocst,
            'rt_tnm_nc_b': relationship.rt_tnm_nc,

            'rt_nm_b': relationship.rt_nm,
            'rt_om_b': relationship.rt_om,

            'remarks_t': relationship.remarks,
            'created_dt': relationship.created,
            'updated_dt': relationship.updated,
            'curated_b': relationship.curated,

            # Information about the model CRIMObservation

            'model_musical_type_s': relationship.model_observation.musical_type,

            'model_observation_id_i': relationship.model_observation.id,
            'model_observer_s': relationship.model_observation.observer.name,
            'model_ema_t': relationship.model_observation.ema,

            'model_mt_cf_b': relationship.model_observation.mt_cf,
            'model_mt_cf_voices_ss': relationship.model_observation.mt_cf_voices.split('\n'),
            'model_mt_cf_dur_b': relationship.model_observation.mt_cf_dur,
            'model_mt_cf_mel_b': relationship.model_observation.mt_cf_mel,

            'model_mt_sog_b': relationship.model_observation.mt_sog,
            'model_mt_sog_voices_ss': relationship.model_observation.mt_sog_voices.split('\n'),
            'model_mt_sog_dur_b': relationship.model_observation.mt_sog_dur,
            'model_mt_sog_mel_b': relationship.model_observation.mt_sog_mel,
            'model_mt_sog_ostinato_b': relationship.model_observation.mt_sog_ostinato,
            'model_mt_sog_periodic_b': relationship.model_observation.mt_sog_periodic,

            'model_mt_csog_b': relationship.model_observation.mt_csog,
            'model_mt_csog_voices_ss': relationship.model_observation.mt_csog_voices.split('\n'),
            'model_mt_csog_dur_b': relationship.model_observation.mt_csog_dur,
            'model_mt_csog_mel_b': relationship.model_observation.mt_csog_mel,

            'model_mt_cd_b': relationship.model_observation.mt_cd,
            'model_mt_cd_voices_ss': relationship.model_observation.mt_cd_voices.split('\n'),

            'model_mt_fg_b': relationship.model_observation.mt_fg,
            'model_mt_fg_voices_ss': relationship.model_observation.mt_fg_voices.split('\n'),
            'model_mt_fg_int_s': relationship.model_observation.mt_fg_int,
            'model_mt_fg_tint_s': relationship.model_observation.mt_fg_tint,
            'model_mt_fg_periodic_b': relationship.model_observation.mt_fg_periodic,
            'model_mt_fg_strict_b': relationship.model_observation.mt_fg_strict,
            'model_mt_fg_flexed_b': relationship.model_observation.mt_fg_flexed,
            'model_mt_fg_sequential_b': relationship.model_observation.mt_fg_sequential,
            'model_mt_fg_inverted_b': relationship.model_observation.mt_fg_inverted,
            'model_mt_fg_retrograde_b': relationship.model_observation.mt_fg_retrograde,

            'model_mt_pe_b': relationship.model_observation.mt_pe,
            'model_mt_pe_voices_ss': relationship.model_observation.mt_pe_voices.split('\n'),
            'model_mt_pe_int_s': relationship.model_observation.mt_pe_int,
            'model_mt_pe_tint_s': relationship.model_observation.mt_pe_tint,
            'model_mt_pe_strict_b': relationship.model_observation.mt_pe_strict,
            'model_mt_pe_flexed_b': relationship.model_observation.mt_pe_flexed,
            'model_mt_pe_flt_b': relationship.model_observation.mt_pe_flt,
            'model_mt_pe_sequential_b': relationship.model_observation.mt_pe_sequential,
            'model_mt_pe_added_b': relationship.model_observation.mt_pe_added,
            'model_mt_pe_invertible_b': relationship.model_observation.mt_pe_invertible,

            'model_mt_id_b': relationship.model_observation.mt_id,
            'model_mt_id_voices_ss': relationship.model_observation.mt_id_voices.split('\n'),
            'model_mt_id_int_s': relationship.model_observation.mt_id_int,
            'model_mt_id_tint_s': relationship.model_observation.mt_id_tint,
            'model_mt_id_strict_b': relationship.model_observation.mt_id_strict,
            'model_mt_id_flexed_b': relationship.model_observation.mt_id_flexed,
            'model_mt_id_flt_b': relationship.model_observation.mt_id_flt,
            'model_mt_id_invertible_b': relationship.model_observation.mt_id_invertible,

            'model_mt_nid_b': relationship.model_observation.mt_nid,
            'model_mt_nid_voices_ss': relationship.model_observation.mt_nid_voices.split('\n'),
            'model_mt_nid_int_s': relationship.model_observation.mt_nid_int,
            'model_mt_nid_tint_s': relationship.model_observation.mt_nid_tint,
            'model_mt_nid_strict_b': relationship.model_observation.mt_nid_strict,
            'model_mt_nid_flexed_b': relationship.model_observation.mt_nid_flexed,
            'model_mt_nid_flt_b': relationship.model_observation.mt_nid_flt,
            'model_mt_nid_sequential_b': relationship.model_observation.mt_nid_sequential,
            'model_mt_nid_invertible_b': relationship.model_observation.mt_nid_invertible,

            'model_mt_hr_b': relationship.model_observation.mt_hr,
            'model_mt_hr_voices_ss': relationship.model_observation.mt_hr_voices.split('\n'),
            'model_mt_hr_simple_b': relationship.model_observation.mt_hr_simple,
            'model_mt_hr_staggered_b': relationship.model_observation.mt_hr_staggered,
            'model_mt_hr_sequential_b': relationship.model_observation.mt_hr_sequential,
            'model_mt_hr_fauxbourdon_b': relationship.model_observation.mt_hr_fauxbourdon,

            'model_mt_cad_b': relationship.model_observation.mt_cad,
            'model_mt_cad_cantizans_s': relationship.model_observation.mt_cad_cantizans,
            'model_mt_cad_tenorizans_s': relationship.model_observation.mt_cad_tenorizans,
            'model_mt_cad_type_s': relationship.model_observation.mt_cad_type,
            'model_mt_cad_tone_s': relationship.model_observation.mt_cad_tone,
            'model_mt_cad_dtv_s': relationship.model_observation.mt_cad_dtv,
            'model_mt_cad_dti_s': relationship.model_observation.mt_cad_dti,

            'model_mt_int_b': relationship.model_observation.mt_int,
            'model_mt_int_voices_ss': relationship.model_observation.mt_int_voices.split('\n'),
            'model_mt_int_p6_b': relationship.model_observation.mt_int_p6,
            'model_mt_int_p3_b': relationship.model_observation.mt_int_p3,
            'model_mt_int_c35_b': relationship.model_observation.mt_int_c35,
            'model_mt_int_c83_b': relationship.model_observation.mt_int_c83,
            'model_mt_int_c65_b': relationship.model_observation.mt_int_c65,

            'model_mt_fp_b': relationship.model_observation.mt_fp,
            'model_mt_fp_ir_b': relationship.model_observation.mt_fp_ir,
            'model_mt_fp_range_s': relationship.model_observation.mt_fp_range,
            'model_mt_fp_comment_t': relationship.model_observation.mt_fp_comment,

            'model_remarks_t': relationship.model_observation.remarks,
            'model_created_dt': relationship.model_observation.created,
            'model_updated_dt': relationship.model_observation.updated,
            'model_curated_b': relationship.model_observation.curated,

            # Information about the model observation's CRIMPiece

            'model_piece_id_s': relationship.model_observation.piece.piece_id,
            'model_title_s': relationship.model_observation.piece.title,
            'model_mass_s': relationship.model_observation.piece.mass.title if relationship.model_observation.piece.mass else None,
            'model_composer_s': relationship.model_observation.piece.composer.name,
            'model_genre_s': relationship.model_observation.piece.genre,
            'model_date_i': relationship.model_observation.piece.date_sort,
            'model_pdf_links_ss': relationship.model_observation.piece.pdf_links.split('\n'),
            'model_mei_links_ss': relationship.model_observation.piece.mei_links.split('\n'),
            'model_remarks_t': relationship.model_observation.piece.remarks,

            # Information about the derivative CRIMObservation

            'derivative_musical_type_s': relationship.derivative_observation.musical_type,

            'derivative_observation_id_i': relationship.derivative_observation.id,
            'derivative_observer_s': relationship.derivative_observation.observer.name,
            'derivative_ema_t': relationship.derivative_observation.ema,

            'derivative_mt_cf_b': relationship.derivative_observation.mt_cf,
            'derivative_mt_cf_voices_ss': relationship.derivative_observation.mt_cf_voices.split('\n'),
            'derivative_mt_cf_dur_b': relationship.derivative_observation.mt_cf_dur,
            'derivative_mt_cf_mel_b': relationship.derivative_observation.mt_cf_mel,

            'derivative_mt_sog_b': relationship.derivative_observation.mt_sog,
            'derivative_mt_sog_voices_ss': relationship.derivative_observation.mt_sog_voices.split('\n'),
            'derivative_mt_sog_dur_b': relationship.derivative_observation.mt_sog_dur,
            'derivative_mt_sog_mel_b': relationship.derivative_observation.mt_sog_mel,
            'derivative_mt_sog_ostinato_b': relationship.derivative_observation.mt_sog_ostinato,
            'derivative_mt_sog_periodic_b': relationship.derivative_observation.mt_sog_periodic,

            'derivative_mt_csog_b': relationship.derivative_observation.mt_csog,
            'derivative_mt_csog_voices_ss': relationship.derivative_observation.mt_csog_voices.split('\n'),
            'derivative_mt_csog_dur_b': relationship.derivative_observation.mt_csog_dur,
            'derivative_mt_csog_mel_b': relationship.derivative_observation.mt_csog_mel,

            'derivative_mt_cd_b': relationship.derivative_observation.mt_cd,
            'derivative_mt_cd_voices_ss': relationship.derivative_observation.mt_cd_voices.split('\n'),

            'derivative_mt_fg_b': relationship.derivative_observation.mt_fg,
            'derivative_mt_fg_voices_ss': relationship.derivative_observation.mt_fg_voices.split('\n'),
            'derivative_mt_fg_int_s': relationship.derivative_observation.mt_fg_int,
            'derivative_mt_fg_tint_s': relationship.derivative_observation.mt_fg_tint,
            'derivative_mt_fg_periodic_b': relationship.derivative_observation.mt_fg_periodic,
            'derivative_mt_fg_strict_b': relationship.derivative_observation.mt_fg_strict,
            'derivative_mt_fg_flexed_b': relationship.derivative_observation.mt_fg_flexed,
            'derivative_mt_fg_sequential_b': relationship.derivative_observation.mt_fg_sequential,
            'derivative_mt_fg_inverted_b': relationship.derivative_observation.mt_fg_inverted,
            'derivative_mt_fg_retrograde_b': relationship.derivative_observation.mt_fg_retrograde,

            'derivative_mt_pe_b': relationship.derivative_observation.mt_pe,
            'derivative_mt_pe_voices_ss': relationship.derivative_observation.mt_pe_voices.split('\n'),
            'derivative_mt_pe_int_s': relationship.derivative_observation.mt_pe_int,
            'derivative_mt_pe_tint_s': relationship.derivative_observation.mt_pe_tint,
            'derivative_mt_pe_strict_b': relationship.derivative_observation.mt_pe_strict,
            'derivative_mt_pe_flexed_b': relationship.derivative_observation.mt_pe_flexed,
            'derivative_mt_pe_flt_b': relationship.derivative_observation.mt_pe_flt,
            'derivative_mt_pe_sequential_b': relationship.derivative_observation.mt_pe_sequential,
            'derivative_mt_pe_added_b': relationship.derivative_observation.mt_pe_added,
            'derivative_mt_pe_invertible_b': relationship.derivative_observation.mt_pe_invertible,

            'derivative_mt_id_b': relationship.derivative_observation.mt_id,
            'derivative_mt_id_voices_ss': relationship.derivative_observation.mt_id_voices.split('\n'),
            'derivative_mt_id_int_s': relationship.derivative_observation.mt_id_int,
            'derivative_mt_id_tint_s': relationship.derivative_observation.mt_id_tint,
            'derivative_mt_id_strict_b': relationship.derivative_observation.mt_id_strict,
            'derivative_mt_id_flexed_b': relationship.derivative_observation.mt_id_flexed,
            'derivative_mt_id_flt_b': relationship.derivative_observation.mt_id_flt,
            'derivative_mt_id_invertible_b': relationship.derivative_observation.mt_id_invertible,

            'derivative_mt_nid_b': relationship.derivative_observation.mt_nid,
            'derivative_mt_nid_voices_ss': relationship.derivative_observation.mt_nid_voices.split('\n'),
            'derivative_mt_nid_int_s': relationship.derivative_observation.mt_nid_int,
            'derivative_mt_nid_tint_s': relationship.derivative_observation.mt_nid_tint,
            'derivative_mt_nid_strict_b': relationship.derivative_observation.mt_nid_strict,
            'derivative_mt_nid_flexed_b': relationship.derivative_observation.mt_nid_flexed,
            'derivative_mt_nid_flt_b': relationship.derivative_observation.mt_nid_flt,
            'derivative_mt_nid_sequential_b': relationship.derivative_observation.mt_nid_sequential,
            'derivative_mt_nid_invertible_b': relationship.derivative_observation.mt_nid_invertible,

            'derivative_mt_hr_b': relationship.derivative_observation.mt_hr,
            'derivative_mt_hr_voices_ss': relationship.derivative_observation.mt_hr_voices.split('\n'),
            'derivative_mt_hr_simple_b': relationship.derivative_observation.mt_hr_simple,
            'derivative_mt_hr_staggered_b': relationship.derivative_observation.mt_hr_staggered,
            'derivative_mt_hr_sequential_b': relationship.derivative_observation.mt_hr_sequential,
            'derivative_mt_hr_fauxbourdon_b': relationship.derivative_observation.mt_hr_fauxbourdon,

            'derivative_mt_cad_b': relationship.derivative_observation.mt_cad,
            'derivative_mt_cad_cantizans_s': relationship.derivative_observation.mt_cad_cantizans,
            'derivative_mt_cad_tenorizans_s': relationship.derivative_observation.mt_cad_tenorizans,
            'derivative_mt_cad_type_s': relationship.derivative_observation.mt_cad_type,
            'derivative_mt_cad_tone_s': relationship.derivative_observation.mt_cad_tone,
            'derivative_mt_cad_dtv_s': relationship.derivative_observation.mt_cad_dtv,
            'derivative_mt_cad_dti_s': relationship.derivative_observation.mt_cad_dti,

            'derivative_mt_int_b': relationship.derivative_observation.mt_int,
            'derivative_mt_int_voices_ss': relationship.derivative_observation.mt_int_voices.split('\n'),
            'derivative_mt_int_p6_b': relationship.derivative_observation.mt_int_p6,
            'derivative_mt_int_p3_b': relationship.derivative_observation.mt_int_p3,
            'derivative_mt_int_c35_b': relationship.derivative_observation.mt_int_c35,
            'derivative_mt_int_c83_b': relationship.derivative_observation.mt_int_c83,
            'derivative_mt_int_c65_b': relationship.derivative_observation.mt_int_c65,

            'derivative_mt_fp_b': relationship.derivative_observation.mt_fp,
            'derivative_mt_fp_ir_b': relationship.derivative_observation.mt_fp_ir,
            'derivative_mt_fp_range_s': relationship.derivative_observation.mt_fp_range,
            'derivative_mt_fp_comment_t': relationship.derivative_observation.mt_fp_comment,

            'derivative_remarks_t': relationship.derivative_observation.remarks,
            'derivative_created_dt': relationship.derivative_observation.created,
            'derivative_updated_dt': relationship.derivative_observation.updated,
            'derivative_curated_b': relationship.derivative_observation.curated,

            # Information about the derivative observation's CRIMPiece

            'derivative_piece_id_s': relationship.derivative_observation.piece.piece_id,
            'derivative_title_s': relationship.derivative_observation.piece.title,
            'derivative_mass_s': relationship.derivative_observation.piece.mass.title if relationship.derivative_observation.piece.mass else None,
            'derivative_composer_s': relationship.derivative_observation.piece.composer.name,
            'derivative_genre_s': relationship.derivative_observation.piece.genre,
            'derivative_date_i': relationship.derivative_observation.piece.date_sort,
            'derivative_pdf_links_ss': relationship.derivative_observation.piece.pdf_links.split('\n'),
            'derivative_mei_links_ss': relationship.derivative_observation.piece.mei_links.split('\n'),
            'derivative_remarks_t': relationship.derivative_observation.piece.remarks,
        }
        solrconn.add(**d, commit=True)
    print('Done adding analyses')

    sys.exit()
