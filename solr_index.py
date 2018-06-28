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
        d = {
            'type': 'crim_relationship',
            'id': relationship.id,
            'observer': relationship.observer.name_sort,

            # Information about the relationship type

            'rt_q': relationship.rt_q,
            'rt_q_x': relationship.rt_q_x,
            'rt_q_monnayage': relationship.rt_q_monnayage,

            'rt_tm': relationship.rt_tm,
            'rt_tm_snd': relationship.rt_tm_snd,
            'rt_tm_minv': relationship.rt_tm_minv,
            'rt_tm_retrograde': relationship.rt_tm_retrograde,
            'rt_tm_ms': relationship.rt_tm_ms,
            'rt_tm_transposed': relationship.rt_tm_transposed,
            'rt_tm_invertible': relationship.rt_tm_invertible,

            'rt_tnm': relationship.rt_tnm,
            'rt_tnm_embellished': relationship.rt_tnm_embellished,
            'rt_tnm_reduced': relationship.rt_tnm_reduced,
            'rt_tnm_amplified': relationship.rt_tnm_amplified,
            'rt_tnm_truncated': relationship.rt_tnm_truncated,
            'rt_tnm_ncs': relationship.rt_tnm_ncs,
            'rt_tnm_ocs': relationship.rt_tnm_ocs,
            'rt_tnm_ocst': relationship.rt_tnm_ocst,
            'rt_tnm_nc': relationship.rt_tnm_nc,

            'rt_nm': relationship.rt_nm,
            'rt_om': relationship.rt_om,

            'remarks': relationship.remarks,
            'created': relationship.created,
            'updated': relationship.updated,
            'status': relationship.status,

            # Information about the model CRIMObservation

            'model_observer': relationship.model_observation.observer.name_sort,
            'model_ema': relationship.model_observation.ema,

            'model_mt_cf': relationship.model_observation.mt_cf,
            'model_mt_cf_voices': relationship.model_observation.mt_cf_voices,
            'model_mt_cf_dur': relationship.model_observation.mt_cf_dur,
            'model_mt_cf_mel': relationship.model_observation.mt_cf_mel,

            'model_mt_sog': relationship.model_observation.mt_sog,
            'model_mt_sog_voices': relationship.model_observation.mt_sog_voices,
            'model_mt_sog_dur': relationship.model_observation.mt_sog_dur,
            'model_mt_sog_mel': relationship.model_observation.mt_sog_mel,
            'model_mt_sog_ostinato': relationship.model_observation.mt_sog_ostinato,
            'model_mt_sog_periodic': relationship.model_observation.mt_sog_periodic,

            'model_mt_csog': relationship.model_observation.mt_csog,
            'model_mt_csog_voices': relationship.model_observation.mt_csog_voices,
            'model_mt_csog_dur': relationship.model_observation.mt_csog_dur,
            'model_mt_csog_mel': relationship.model_observation.mt_csog_mel,

            'model_mt_cd': relationship.model_observation.mt_cd,
            'model_mt_cd_voices': relationship.model_observation.mt_cd_voices,

            'model_mt_fg': relationship.model_observation.mt_fg,
            'model_mt_fg_voices': relationship.model_observation.mt_fg_voices,
            'model_mt_fg_periodic': relationship.model_observation.mt_fg_periodic,
            'model_mt_fg_strict': relationship.model_observation.mt_fg_strict,
            'model_mt_fg_flexed': relationship.model_observation.mt_fg_flexed,
            'model_mt_fg_sequential': relationship.model_observation.mt_fg_sequential,
            'model_mt_fg_inverted': relationship.model_observation.mt_fg_inverted,
            'model_mt_fg_retrograde': relationship.model_observation.mt_fg_retrograde,
            'model_mt_fg_int': relationship.model_observation.mt_fg_int,
            'model_mt_fg_tint': relationship.model_observation.mt_fg_tint,

            'model_mt_id': relationship.model_observation.mt_id,
            'model_mt_id_voices': relationship.model_observation.mt_id_voices,
            'model_mt_id_strict': relationship.model_observation.mt_id_strict,
            'model_mt_id_flexed': relationship.model_observation.mt_id_flexed,
            'model_mt_id_flt': relationship.model_observation.mt_id_flt,
            'model_mt_id_invertible': relationship.model_observation.mt_id_invertible,
            'model_mt_id_int': relationship.model_observation.mt_id_int,
            'model_mt_id_tint': relationship.model_observation.mt_id_tint,

            'model_mt_pe': relationship.model_observation.mt_pe,
            'model_mt_pe_voices': relationship.model_observation.mt_pe_voices,
            'model_mt_pe_strict': relationship.model_observation.mt_pe_strict,
            'model_mt_pe_flexed': relationship.model_observation.mt_pe_flexed,
            'model_mt_pe_flt': relationship.model_observation.mt_pe_flt,
            'model_mt_pe_sequential': relationship.model_observation.mt_pe_sequential,
            'model_mt_pe_added': relationship.model_observation.mt_pe_added,
            'model_mt_pe_invertible': relationship.model_observation.mt_pe_invertible,
            'model_mt_pe_int': relationship.model_observation.mt_pe_int,
            'model_mt_pe_tint': relationship.model_observation.mt_pe_tint,

            'model_mt_nid': relationship.model_observation.mt_nid,
            'model_mt_nid_voices': relationship.model_observation.mt_nid_voices,
            'model_mt_nid_strict': relationship.model_observation.mt_nid_strict,
            'model_mt_nid_flexed': relationship.model_observation.mt_nid_flexed,
            'model_mt_nid_flt': relationship.model_observation.mt_nid_flt,
            'model_mt_nid_sequential': relationship.model_observation.mt_nid_sequential,
            'model_mt_nid_invertible': relationship.model_observation.mt_nid_invertible,
            'model_mt_nid_int': relationship.model_observation.mt_nid_int,
            'model_mt_nid_tint': relationship.model_observation.mt_nid_tint,

            'model_mt_hr': relationship.model_observation.mt_hr,
            'model_mt_hr_voices': relationship.model_observation.mt_hr_voices,
            'model_mt_hr_simple': relationship.model_observation.mt_hr_simple,
            'model_mt_hr_staggered': relationship.model_observation.mt_hr_staggered,
            'model_mt_hr_sequential': relationship.model_observation.mt_hr_sequential,
            'model_mt_hr_fauxbourdon': relationship.model_observation.mt_hr_fauxbourdon,

            'model_mt_cad': relationship.model_observation.mt_cad,
            'model_mt_cad_cantizans': relationship.model_observation.mt_cad_cantizans,
            'model_mt_cad_tenorizans': relationship.model_observation.mt_cad_tenorizans,
            'model_mt_cad_authentic': relationship.model_observation.mt_cad_authentic,
            'model_mt_cad_phrygian': relationship.model_observation.mt_cad_phrygian,
            'model_mt_cad_plagal': relationship.model_observation.mt_cad_plagal,
            'model_mt_cad_tone': relationship.model_observation.mt_cad_tone,
            'model_mt_cad_dtv': relationship.model_observation.mt_cad_dtv,
            'model_mt_cad_dti': relationship.model_observation.mt_cad_dti,

            'model_mt_int': relationship.model_observation.mt_int,
            'model_mt_int_voices': relationship.model_observation.mt_int_voices,
            'model_mt_int_p6': relationship.model_observation.mt_int_p6,
            'model_mt_int_p3': relationship.model_observation.mt_int_p3,
            'model_mt_int_c35': relationship.model_observation.mt_int_c35,
            'model_mt_int_c83': relationship.model_observation.mt_int_c83,
            'model_mt_int_c65': relationship.model_observation.mt_int_c65,

            'model_mt_fp': relationship.model_observation.mt_fp,
            'model_mt_fp_comment': relationship.model_observation.mt_fp_comment,
            'model_mt_fp_ir': relationship.model_observation.mt_fp_ir,
            'model_mt_fp_range': relationship.model_observation.mt_fp_range,

            'model_remarks': relationship.model_observation.remarks,
            'model_created': relationship.model_observation.created,
            'model_updated': relationship.model_observation.updated,
            'model_status': relationship.model_observation.status,

            # Information about the model observation's CRIMPiece

            'model_piece_id': relationship.model_observation.piece.piece_id,
            'model_title': relationship.model_observation.piece.title,
            'model_mass_title': relationship.model_observation.piece.mass.title if relationship.model_observation.piece.mass else None,
            'model_composer': relationship.model_observation.piece.composer.name_sort,
            'model_genre': relationship.model_observation.piece.genre,
            'model_date': relationship.model_observation.piece.date_sort,
            'model_pdf_links': relationship.model_observation.piece.pdf_links,
            'model_mei_links': relationship.model_observation.piece.mei_links,
            'model_remarks': relationship.model_observation.piece.remarks,

            # Information about the derivative CRIMObservation

            'derivative_observer': relationship.derivative_observation.observer.name_sort,
            'derivative_ema': relationship.derivative_observation.ema,

            'derivative_mt_cf': relationship.derivative_observation.mt_cf,
            'derivative_mt_cf_voices': relationship.derivative_observation.mt_cf_voices,
            'derivative_mt_cf_dur': relationship.derivative_observation.mt_cf_dur,
            'derivative_mt_cf_mel': relationship.derivative_observation.mt_cf_mel,

            'derivative_mt_sog': relationship.derivative_observation.mt_sog,
            'derivative_mt_sog_voices': relationship.derivative_observation.mt_sog_voices,
            'derivative_mt_sog_dur': relationship.derivative_observation.mt_sog_dur,
            'derivative_mt_sog_mel': relationship.derivative_observation.mt_sog_mel,
            'derivative_mt_sog_ostinato': relationship.derivative_observation.mt_sog_ostinato,
            'derivative_mt_sog_periodic': relationship.derivative_observation.mt_sog_periodic,

            'derivative_mt_csog': relationship.derivative_observation.mt_csog,
            'derivative_mt_csog_voices': relationship.derivative_observation.mt_csog_voices,
            'derivative_mt_csog_dur': relationship.derivative_observation.mt_csog_dur,
            'derivative_mt_csog_mel': relationship.derivative_observation.mt_csog_mel,

            'derivative_mt_cd': relationship.derivative_observation.mt_cd,
            'derivative_mt_cd_voices': relationship.derivative_observation.mt_cd_voices,

            'derivative_mt_fg': relationship.derivative_observation.mt_fg,
            'derivative_mt_fg_voices': relationship.derivative_observation.mt_fg_voices,
            'derivative_mt_fg_periodic': relationship.derivative_observation.mt_fg_periodic,
            'derivative_mt_fg_strict': relationship.derivative_observation.mt_fg_strict,
            'derivative_mt_fg_flexed': relationship.derivative_observation.mt_fg_flexed,
            'derivative_mt_fg_sequential': relationship.derivative_observation.mt_fg_sequential,
            'derivative_mt_fg_inverted': relationship.derivative_observation.mt_fg_inverted,
            'derivative_mt_fg_retrograde': relationship.derivative_observation.mt_fg_retrograde,
            'derivative_mt_fg_int': relationship.derivative_observation.mt_fg_int,
            'derivative_mt_fg_tint': relationship.derivative_observation.mt_fg_tint,

            'derivative_mt_id': relationship.derivative_observation.mt_id,
            'derivative_mt_id_voices': relationship.derivative_observation.mt_id_voices,
            'derivative_mt_id_strict': relationship.derivative_observation.mt_id_strict,
            'derivative_mt_id_flexed': relationship.derivative_observation.mt_id_flexed,
            'derivative_mt_id_flt': relationship.derivative_observation.mt_id_flt,
            'derivative_mt_id_invertible': relationship.derivative_observation.mt_id_invertible,
            'derivative_mt_id_int': relationship.derivative_observation.mt_id_int,
            'derivative_mt_id_tint': relationship.derivative_observation.mt_id_tint,

            'derivative_mt_pe': relationship.derivative_observation.mt_pe,
            'derivative_mt_pe_voices': relationship.derivative_observation.mt_pe_voices,
            'derivative_mt_pe_strict': relationship.derivative_observation.mt_pe_strict,
            'derivative_mt_pe_flexed': relationship.derivative_observation.mt_pe_flexed,
            'derivative_mt_pe_flt': relationship.derivative_observation.mt_pe_flt,
            'derivative_mt_pe_sequential': relationship.derivative_observation.mt_pe_sequential,
            'derivative_mt_pe_added': relationship.derivative_observation.mt_pe_added,
            'derivative_mt_pe_invertible': relationship.derivative_observation.mt_pe_invertible,
            'derivative_mt_pe_int': relationship.derivative_observation.mt_pe_int,
            'derivative_mt_pe_tint': relationship.derivative_observation.mt_pe_tint,

            'derivative_mt_nid': relationship.derivative_observation.mt_nid,
            'derivative_mt_nid_voices': relationship.derivative_observation.mt_nid_voices,
            'derivative_mt_nid_strict': relationship.derivative_observation.mt_nid_strict,
            'derivative_mt_nid_flexed': relationship.derivative_observation.mt_nid_flexed,
            'derivative_mt_nid_flt': relationship.derivative_observation.mt_nid_flt,
            'derivative_mt_nid_sequential': relationship.derivative_observation.mt_nid_sequential,
            'derivative_mt_nid_invertible': relationship.derivative_observation.mt_nid_invertible,
            'derivative_mt_nid_int': relationship.derivative_observation.mt_nid_int,
            'derivative_mt_nid_tint': relationship.derivative_observation.mt_nid_tint,

            'derivative_mt_hr': relationship.derivative_observation.mt_hr,
            'derivative_mt_hr_voices': relationship.derivative_observation.mt_hr_voices,
            'derivative_mt_hr_simple': relationship.derivative_observation.mt_hr_simple,
            'derivative_mt_hr_staggered': relationship.derivative_observation.mt_hr_staggered,
            'derivative_mt_hr_sequential': relationship.derivative_observation.mt_hr_sequential,
            'derivative_mt_hr_fauxbourdon': relationship.derivative_observation.mt_hr_fauxbourdon,

            'derivative_mt_cad': relationship.derivative_observation.mt_cad,
            'derivative_mt_cad_cantizans': relationship.derivative_observation.mt_cad_cantizans,
            'derivative_mt_cad_tenorizans': relationship.derivative_observation.mt_cad_tenorizans,
            'derivative_mt_cad_authentic': relationship.derivative_observation.mt_cad_authentic,
            'derivative_mt_cad_phrygian': relationship.derivative_observation.mt_cad_phrygian,
            'derivative_mt_cad_plagal': relationship.derivative_observation.mt_cad_plagal,
            'derivative_mt_cad_tone': relationship.derivative_observation.mt_cad_tone,
            'derivative_mt_cad_dtv': relationship.derivative_observation.mt_cad_dtv,
            'derivative_mt_cad_dti': relationship.derivative_observation.mt_cad_dti,

            'derivative_mt_int': relationship.derivative_observation.mt_int,
            'derivative_mt_int_voices': relationship.derivative_observation.mt_int_voices,
            'derivative_mt_int_p6': relationship.derivative_observation.mt_int_p6,
            'derivative_mt_int_p3': relationship.derivative_observation.mt_int_p3,
            'derivative_mt_int_c35': relationship.derivative_observation.mt_int_c35,
            'derivative_mt_int_c83': relationship.derivative_observation.mt_int_c83,
            'derivative_mt_int_c65': relationship.derivative_observation.mt_int_c65,

            'derivative_mt_fp': relationship.derivative_observation.mt_fp,
            'derivative_mt_fp_comment': relationship.derivative_observation.mt_fp_comment,
            'derivative_mt_fp_ir': relationship.derivative_observation.mt_fp_ir,
            'derivative_mt_fp_range': relationship.derivative_observation.mt_fp_range,

            'derivative_remarks': relationship.derivative_observation.remarks,
            'derivative_created': relationship.derivative_observation.created,
            'derivative_updated': relationship.derivative_observation.updated,
            'derivative_status': relationship.derivative_observation.status,

            # Information about the derivative observation's CRIMPiece

            'derivative_piece_id': relationship.derivative_observation.piece.piece_id,
            'derivative_title': relationship.derivative_observation.piece.title,
            'derivative_mass_title': relationship.derivative_observation.piece.mass.title if relationship.derivative_observation.piece.mass else None,
            'derivative_composer': relationship.derivative_observation.piece.composer.name_sort,
            'derivative_genre': relationship.derivative_observation.piece.genre,
            'derivative_date': relationship.derivative_observation.piece.date_sort,
            'derivative_pdf_links': relationship.derivative_observation.piece.pdf_links,
            'derivative_mei_links': relationship.derivative_observation.piece.mei_links,
            'derivative_remarks': relationship.derivative_observation.piece.remarks,
        }
        solrconn.add(**d)
        if i % 100 == 0:
            solrconn.commit()
    solrconn.commit()
    print('Done adding analyses')

    sys.exit()
