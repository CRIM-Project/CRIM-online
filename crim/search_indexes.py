from haystack import indexes
# from crim.models.piece import CRIMPiece
from crim.models.relationship import CRIMRelationship


# class CRIMPieceIndex(indexes.SearchIndex, indexes.Indexable):
#     '''This indexes all the CRIMPiece objects. However, it is
#     not used in production because we search for CRIMRelationship
#     objects instead. It was used as a simpler text case and
#     is left here in case searching for pieces directly ends
#     up being useful.
#     '''
#     text = indexes.CharField(document=True, use_template=True)
#     piece_id = indexes.CharField(model_attr='piece_id')
#     title = indexes.CharField(model_attr='title')
#     mass_title = indexes.CharField(model_attr='mass__title', null=True)
#     composer = indexes.CharField(model_attr='composer__name_sort', faceted=True, null=True)
#     genre = indexes.CharField(model_attr='genre__name', faceted=True)
#     date = indexes.IntegerField(model_attr='date_sort', faceted=True, null=True)
#     pdf_links = indexes.CharField(model_attr='pdf_links', null=True, indexed=False)
#     mei_links = indexes.CharField(model_attr='mei_links', null=True, indexed=False)
#     remarks = indexes.CharField(model_attr='remarks', null=True, indexed=False)
#
#     def get_model(self):
#         return CRIMPiece


class CRIMRelationshipIndex(indexes.SearchIndex, indexes.Indexable):
    '''This indexes all CRIMRelationship objects.'''

    text = indexes.CharField(document=True, use_template=True)

    # Information about the CRIMRelationship object itself

    relationship_id = indexes.IntegerField(model_attr='id', null=False)
    observer_person_id = indexes.CharField(model_attr='observer__person_id', null=False)
    observer_name_sort = indexes.CharField(model_attr='observer__name_sort', faceted=True, null=False)

    rt_q = indexes.BooleanField(model_attr='rt_q', faceted=True)
    rt_q_exact = indexes.BooleanField(model_attr='rt_q_exact', faceted=True)
    rt_q_monnayage = indexes.BooleanField(model_attr='rt_q_monnayage', faceted=True)

    rt_tm = indexes.BooleanField(model_attr='rt_tm', faceted=True)
    rt_tm_snd = indexes.BooleanField(model_attr='rt_tm_snd', faceted=True)
    rt_tm_minv = indexes.BooleanField(model_attr='rt_tm_minv', faceted=True)
    rt_tm_retrograde = indexes.BooleanField(model_attr='rt_tm_retrograde', faceted=True)
    rt_tm_ms = indexes.BooleanField(model_attr='rt_tm_ms', faceted=True)
    rt_tm_transposed = indexes.BooleanField(model_attr='rt_tm_transposed', faceted=True)
    rt_tm_invertible = indexes.BooleanField(model_attr='rt_tm_invertible', faceted=True)

    rt_tnm = indexes.BooleanField(model_attr='rt_tnm', faceted=True)
    rt_tnm_embellished = indexes.BooleanField(model_attr='rt_tnm_embellished', faceted=True)
    rt_tnm_reduced = indexes.BooleanField(model_attr='rt_tnm_reduced', faceted=True)
    rt_tnm_amplified = indexes.BooleanField(model_attr='rt_tnm_amplified', faceted=True)
    rt_tnm_truncated = indexes.BooleanField(model_attr='rt_tnm_truncated', faceted=True)
    rt_tnm_ncs = indexes.BooleanField(model_attr='rt_tnm_ncs', faceted=True)
    rt_tnm_ocs = indexes.BooleanField(model_attr='rt_tnm_ocs', faceted=True)
    rt_tnm_ocst = indexes.BooleanField(model_attr='rt_tnm_ocst', faceted=True)
    rt_tnm_nc = indexes.BooleanField(model_attr='rt_tnm_nc', faceted=True)

    rt_nm = indexes.BooleanField(model_attr='rt_nm', faceted=True)
    rt_om = indexes.BooleanField(model_attr='rt_om', faceted=True)

    remarks = indexes.CharField(model_attr='remarks', null=True, indexed=False)
    created = indexes.DateTimeField(model_attr='created')
    updated = indexes.DateTimeField(model_attr='updated')
    status = indexes.BooleanField(model_attr='status')

    # Information about the model CRIMObservation

    model_observer_person_id = indexes.CharField(model_attr='model_observation__observer__person_id', faceted=True)
    model_observer_name_sort = indexes.CharField(model_attr='model_observation__observer__name_sort', faceted=True)

    model_ema = indexes.CharField(model_attr='model_observation__ema')

    model_mt_cf = indexes.BooleanField(model_attr='model_observation__mt_cf', faceted=True)
    model_mt_cf_voices = indexes.CharField(model_attr='model_observation__mt_cf_voices')
    model_mt_cf_dur = indexes.BooleanField(model_attr='model_observation__mt_cf_dur', faceted=True)
    model_mt_cf_mel = indexes.BooleanField(model_attr='model_observation__mt_cf_mel', faceted=True)

    model_mt_sog = indexes.BooleanField(model_attr='model_observation__mt_sog', faceted=True)
    model_mt_sog_voices = indexes.CharField(model_attr='model_observation__mt_sog_voices')
    model_mt_sog_dur = indexes.BooleanField(model_attr='model_observation__mt_sog_dur', faceted=True)
    model_mt_sog_mel = indexes.BooleanField(model_attr='model_observation__mt_sog_mel', faceted=True)
    model_mt_sog_ostinato = indexes.BooleanField(model_attr='model_observation__mt_sog_ostinato', faceted=True)
    model_mt_sog_periodic = indexes.BooleanField(model_attr='model_observation__mt_sog_periodic', faceted=True)

    model_mt_csog = indexes.BooleanField(model_attr='model_observation__mt_csog', faceted=True)
    model_mt_csog_voices = indexes.CharField(model_attr='model_observation__mt_csog_voices')
    model_mt_csog_dur = indexes.BooleanField(model_attr='model_observation__mt_csog_dur', faceted=True)
    model_mt_csog_mel = indexes.BooleanField(model_attr='model_observation__mt_csog_mel', faceted=True)

    model_mt_cd = indexes.BooleanField(model_attr='model_observation__mt_cd', faceted=True)
    model_mt_cd_voices = indexes.CharField(model_attr='model_observation__mt_cd_voices')

    model_mt_fg = indexes.BooleanField(model_attr='model_observation__mt_fg', faceted=True)
    model_mt_fg_voices = indexes.CharField(model_attr='model_observation__mt_fg_voices')
    model_mt_fg_periodic = indexes.BooleanField(model_attr='model_observation__mt_fg_periodic', faceted=True)
    model_mt_fg_strict = indexes.BooleanField(model_attr='model_observation__mt_fg_strict', faceted=True)
    model_mt_fg_flexed = indexes.BooleanField(model_attr='model_observation__mt_fg_flexed', faceted=True)
    model_mt_fg_sequential = indexes.BooleanField(model_attr='model_observation__mt_fg_sequential', faceted=True)
    model_mt_fg_inverted = indexes.BooleanField(model_attr='model_observation__mt_fg_inverted', faceted=True)
    model_mt_fg_retrograde = indexes.BooleanField(model_attr='model_observation__mt_fg_retrograde', faceted=True)
    model_mt_fg_int = indexes.CharField(model_attr='model_observation__mt_fg_int')
    model_mt_fg_tint = indexes.CharField(model_attr='model_observation__mt_fg_tint')

    model_mt_id = indexes.BooleanField(model_attr='model_observation__mt_id', faceted=True)
    model_mt_id_voices = indexes.CharField(model_attr='model_observation__mt_id_voices')
    model_mt_id_strict = indexes.BooleanField(model_attr='model_observation__mt_id_strict', faceted=True)
    model_mt_id_flexed = indexes.BooleanField(model_attr='model_observation__mt_id_flexed', faceted=True)
    model_mt_id_flt = indexes.BooleanField(model_attr='model_observation__mt_id_flt', faceted=True)
    model_mt_id_invertible = indexes.BooleanField(model_attr='model_observation__mt_id_invertible', faceted=True)
    model_mt_id_int = indexes.CharField(model_attr='model_observation__mt_id_int')
    model_mt_id_tint = indexes.CharField(model_attr='model_observation__mt_id_tint')

    model_mt_pe = indexes.BooleanField(model_attr='model_observation__mt_pe', faceted=True)
    model_mt_pe_voices = indexes.CharField(model_attr='model_observation__mt_pe_voices')
    model_mt_pe_strict = indexes.BooleanField(model_attr='model_observation__mt_pe_strict', faceted=True)
    model_mt_pe_flexed = indexes.BooleanField(model_attr='model_observation__mt_pe_flexed', faceted=True)
    model_mt_pe_flt = indexes.BooleanField(model_attr='model_observation__mt_pe_flt', faceted=True)
    model_mt_pe_sequential = indexes.BooleanField(model_attr='model_observation__mt_pe_sequential', faceted=True)
    model_mt_pe_added = indexes.BooleanField(model_attr='model_observation__mt_pe_added', faceted=True)
    model_mt_pe_invertible = indexes.BooleanField(model_attr='model_observation__mt_pe_invertible', faceted=True)
    model_mt_pe_int = indexes.CharField(model_attr='model_observation__mt_pe_int')
    model_mt_pe_tint = indexes.CharField(model_attr='model_observation__mt_pe_tint')

    model_mt_nid = indexes.BooleanField(model_attr='model_observation__mt_nid', faceted=True)
    model_mt_nid_voices = indexes.CharField(model_attr='model_observation__mt_nid_voices')
    model_mt_nid_strict = indexes.BooleanField(model_attr='model_observation__mt_nid_strict', faceted=True)
    model_mt_nid_flexed = indexes.BooleanField(model_attr='model_observation__mt_nid_flexed', faceted=True)
    model_mt_nid_flt = indexes.BooleanField(model_attr='model_observation__mt_nid_flt', faceted=True)
    model_mt_nid_sequential = indexes.BooleanField(model_attr='model_observation__mt_nid_sequential', faceted=True)
    model_mt_nid_invertible = indexes.BooleanField(model_attr='model_observation__mt_nid_invertible', faceted=True)
    model_mt_nid_int = indexes.CharField(model_attr='model_observation__mt_nid_int')
    model_mt_nid_tint = indexes.CharField(model_attr='model_observation__mt_nid_tint')

    model_mt_hr = indexes.BooleanField(model_attr='model_observation__mt_hr', faceted=True)
    model_mt_hr_voices = indexes.CharField(model_attr='model_observation__mt_hr_voices')
    model_mt_hr_simple = indexes.BooleanField(model_attr='model_observation__mt_hr_simple', faceted=True)
    model_mt_hr_staggered = indexes.BooleanField(model_attr='model_observation__mt_hr_staggered', faceted=True)
    model_mt_hr_sequential = indexes.BooleanField(model_attr='model_observation__mt_hr_sequential', faceted=True)
    model_mt_hr_fauxbourdon = indexes.BooleanField(model_attr='model_observation__mt_hr_fauxbourdon', faceted=True)

    model_mt_cad = indexes.BooleanField(model_attr='model_observation__mt_cad', faceted=True)
    model_mt_cad_cantizans = indexes.CharField(model_attr='model_observation__mt_cad_cantizans')
    model_mt_cad_tenorizans = indexes.CharField(model_attr='model_observation__mt_cad_tenorizans')
    model_mt_cad_authentic = indexes.BooleanField(model_attr='model_observation__mt_cad_authentic', faceted=True)
    model_mt_cad_phrygian = indexes.BooleanField(model_attr='model_observation__mt_cad_phrygian', faceted=True)
    model_mt_cad_plagal = indexes.BooleanField(model_attr='model_observation__mt_cad_plagal', faceted=True)
    model_mt_cad_tone = indexes.CharField(model_attr='model_observation__mt_cad_tone')
    model_mt_cad_dtv = indexes.CharField(model_attr='model_observation__mt_cad_dtv')
    model_mt_cad_dti = indexes.CharField(model_attr='model_observation__mt_cad_dti')

    model_mt_int = indexes.BooleanField(model_attr='model_observation__mt_int', faceted=True)
    model_mt_int_voices = indexes.CharField(model_attr='model_observation__mt_int_voices')
    model_mt_int_p6 = indexes.BooleanField(model_attr='model_observation__mt_int_p6', faceted=True)
    model_mt_int_p3 = indexes.BooleanField(model_attr='model_observation__mt_int_p3', faceted=True)
    model_mt_int_c35 = indexes.BooleanField(model_attr='model_observation__mt_int_c35', faceted=True)
    model_mt_int_c83 = indexes.BooleanField(model_attr='model_observation__mt_int_c83', faceted=True)
    model_mt_int_c65 = indexes.BooleanField(model_attr='model_observation__mt_int_c65', faceted=True)

    model_mt_fp = indexes.BooleanField(model_attr='model_observation__mt_fp', faceted=True)
    model_mt_fp_comment = indexes.CharField(model_attr='model_observation__mt_fp_comment')
    model_mt_fp_ir = indexes.BooleanField(model_attr='model_observation__mt_fp_ir', faceted=True)
    model_mt_fp_range = indexes.CharField(model_attr='model_observation__mt_fp_range')

    model_remarks = indexes.CharField(model_attr='model_observation__remarks', indexed=False)
    model_created = indexes.DateTimeField(model_attr='model_observation__created')
    model_updated = indexes.DateTimeField(model_attr='model_observation__updated')
    model_status = indexes.BooleanField(model_attr='model_observation__status')

    # Information about the model observation's CRIMPiece

    model_piece_id = indexes.CharField(model_attr='model_observation__piece__piece_id')
    model_title = indexes.CharField(model_attr='model_observation__piece__title')
    model_mass_title = indexes.CharField(model_attr='model_observation__piece__mass__title', null=True)
    model_composer = indexes.CharField(model_attr='model_observation__piece__composer__name_sort', faceted=True, null=True)
    model_genre = indexes.CharField(model_attr='model_observation__piece__genre__name', faceted=True)
    model_date = indexes.IntegerField(model_attr='model_observation__piece__date_sort', faceted=True, null=True)
    model_pdf_links = indexes.CharField(model_attr='model_observation__piece__pdf_links', null=True, indexed=False)
    model_mei_links = indexes.CharField(model_attr='model_observation__piece__mei_links', null=True, indexed=False)
    model_remarks = indexes.CharField(model_attr='model_observation__piece__remarks', null=True, indexed=False)

    # Information about the derivative CRIMObservation

    derivative_observer_person_id = indexes.CharField(model_attr='derivative_observation__observer__person_id', faceted=True)
    derivative_observer_name_sort = indexes.CharField(model_attr='derivative_observation__observer__name_sort', faceted=True)

    derivative_ema = indexes.CharField(model_attr='derivative_observation__ema')

    derivative_mt_cf = indexes.BooleanField(model_attr='derivative_observation__mt_cf', faceted=True)
    derivative_mt_cf_voices = indexes.CharField(model_attr='derivative_observation__mt_cf_voices')
    derivative_mt_cf_dur = indexes.BooleanField(model_attr='derivative_observation__mt_cf_dur', faceted=True)
    derivative_mt_cf_mel = indexes.BooleanField(model_attr='derivative_observation__mt_cf_mel', faceted=True)

    derivative_mt_sog = indexes.BooleanField(model_attr='derivative_observation__mt_sog', faceted=True)
    derivative_mt_sog_voices = indexes.CharField(model_attr='derivative_observation__mt_sog_voices')
    derivative_mt_sog_dur = indexes.BooleanField(model_attr='derivative_observation__mt_sog_dur', faceted=True)
    derivative_mt_sog_mel = indexes.BooleanField(model_attr='derivative_observation__mt_sog_mel', faceted=True)
    derivative_mt_sog_ostinato = indexes.BooleanField(model_attr='derivative_observation__mt_sog_ostinato', faceted=True)
    derivative_mt_sog_periodic = indexes.BooleanField(model_attr='derivative_observation__mt_sog_periodic', faceted=True)

    derivative_mt_csog = indexes.BooleanField(model_attr='derivative_observation__mt_csog', faceted=True)
    derivative_mt_csog_voices = indexes.CharField(model_attr='derivative_observation__mt_csog_voices')
    derivative_mt_csog_dur = indexes.BooleanField(model_attr='derivative_observation__mt_csog_dur', faceted=True)
    derivative_mt_csog_mel = indexes.BooleanField(model_attr='derivative_observation__mt_csog_mel', faceted=True)

    derivative_mt_cd = indexes.BooleanField(model_attr='derivative_observation__mt_cd', faceted=True)
    derivative_mt_cd_voices = indexes.CharField(model_attr='derivative_observation__mt_cd_voices')

    derivative_mt_fg = indexes.BooleanField(model_attr='derivative_observation__mt_fg', faceted=True)
    derivative_mt_fg_voices = indexes.CharField(model_attr='derivative_observation__mt_fg_voices')
    derivative_mt_fg_periodic = indexes.BooleanField(model_attr='derivative_observation__mt_fg_periodic', faceted=True)
    derivative_mt_fg_strict = indexes.BooleanField(model_attr='derivative_observation__mt_fg_strict', faceted=True)
    derivative_mt_fg_flexed = indexes.BooleanField(model_attr='derivative_observation__mt_fg_flexed', faceted=True)
    derivative_mt_fg_sequential = indexes.BooleanField(model_attr='derivative_observation__mt_fg_sequential', faceted=True)
    derivative_mt_fg_inverted = indexes.BooleanField(model_attr='derivative_observation__mt_fg_inverted', faceted=True)
    derivative_mt_fg_retrograde = indexes.BooleanField(model_attr='derivative_observation__mt_fg_retrograde', faceted=True)
    derivative_mt_fg_int = indexes.CharField(model_attr='derivative_observation__mt_fg_int')
    derivative_mt_fg_tint = indexes.CharField(model_attr='derivative_observation__mt_fg_tint')

    derivative_mt_id = indexes.BooleanField(model_attr='derivative_observation__mt_id', faceted=True)
    derivative_mt_id_voices = indexes.CharField(model_attr='derivative_observation__mt_id_voices')
    derivative_mt_id_strict = indexes.BooleanField(model_attr='derivative_observation__mt_id_strict', faceted=True)
    derivative_mt_id_flexed = indexes.BooleanField(model_attr='derivative_observation__mt_id_flexed', faceted=True)
    derivative_mt_id_flt = indexes.BooleanField(model_attr='derivative_observation__mt_id_flt', faceted=True)
    derivative_mt_id_invertible = indexes.BooleanField(model_attr='derivative_observation__mt_id_invertible', faceted=True)
    derivative_mt_id_int = indexes.CharField(model_attr='derivative_observation__mt_id_int')
    derivative_mt_id_tint = indexes.CharField(model_attr='derivative_observation__mt_id_tint')

    derivative_mt_pe = indexes.BooleanField(model_attr='derivative_observation__mt_pe', faceted=True)
    derivative_mt_pe_voices = indexes.CharField(model_attr='derivative_observation__mt_pe_voices')
    derivative_mt_pe_strict = indexes.BooleanField(model_attr='derivative_observation__mt_pe_strict', faceted=True)
    derivative_mt_pe_flexed = indexes.BooleanField(model_attr='derivative_observation__mt_pe_flexed', faceted=True)
    derivative_mt_pe_flt = indexes.BooleanField(model_attr='derivative_observation__mt_pe_flt', faceted=True)
    derivative_mt_pe_sequential = indexes.BooleanField(model_attr='derivative_observation__mt_pe_sequential', faceted=True)
    derivative_mt_pe_added = indexes.BooleanField(model_attr='derivative_observation__mt_pe_added', faceted=True)
    derivative_mt_pe_invertible = indexes.BooleanField(model_attr='derivative_observation__mt_pe_invertible', faceted=True)
    derivative_mt_pe_int = indexes.CharField(model_attr='derivative_observation__mt_pe_int')
    derivative_mt_pe_tint = indexes.CharField(model_attr='derivative_observation__mt_pe_tint')

    derivative_mt_nid = indexes.BooleanField(model_attr='derivative_observation__mt_nid', faceted=True)
    derivative_mt_nid_voices = indexes.CharField(model_attr='derivative_observation__mt_nid_voices')
    derivative_mt_nid_strict = indexes.BooleanField(model_attr='derivative_observation__mt_nid_strict', faceted=True)
    derivative_mt_nid_flexed = indexes.BooleanField(model_attr='derivative_observation__mt_nid_flexed', faceted=True)
    derivative_mt_nid_flt = indexes.BooleanField(model_attr='derivative_observation__mt_nid_flt', faceted=True)
    derivative_mt_nid_sequential = indexes.BooleanField(model_attr='derivative_observation__mt_nid_sequential', faceted=True)
    derivative_mt_nid_invertible = indexes.BooleanField(model_attr='derivative_observation__mt_nid_invertible', faceted=True)
    derivative_mt_nid_int = indexes.CharField(model_attr='derivative_observation__mt_nid_int')
    derivative_mt_nid_tint = indexes.CharField(model_attr='derivative_observation__mt_nid_tint')

    derivative_mt_hr = indexes.BooleanField(model_attr='derivative_observation__mt_hr', faceted=True)
    derivative_mt_hr_voices = indexes.CharField(model_attr='derivative_observation__mt_hr_voices')
    derivative_mt_hr_simple = indexes.BooleanField(model_attr='derivative_observation__mt_hr_simple', faceted=True)
    derivative_mt_hr_staggered = indexes.BooleanField(model_attr='derivative_observation__mt_hr_staggered', faceted=True)
    derivative_mt_hr_sequential = indexes.BooleanField(model_attr='derivative_observation__mt_hr_sequential', faceted=True)
    derivative_mt_hr_fauxbourdon = indexes.BooleanField(model_attr='derivative_observation__mt_hr_fauxbourdon', faceted=True)

    derivative_mt_cad = indexes.BooleanField(model_attr='derivative_observation__mt_cad', faceted=True)
    derivative_mt_cad_cantizans = indexes.CharField(model_attr='derivative_observation__mt_cad_cantizans')
    derivative_mt_cad_tenorizans = indexes.CharField(model_attr='derivative_observation__mt_cad_tenorizans')
    derivative_mt_cad_authentic = indexes.BooleanField(model_attr='derivative_observation__mt_cad_authentic', faceted=True)
    derivative_mt_cad_phrygian = indexes.BooleanField(model_attr='derivative_observation__mt_cad_phrygian', faceted=True)
    derivative_mt_cad_plagal = indexes.BooleanField(model_attr='derivative_observation__mt_cad_plagal', faceted=True)
    derivative_mt_cad_tone = indexes.CharField(model_attr='derivative_observation__mt_cad_tone')
    derivative_mt_cad_dtv = indexes.CharField(model_attr='derivative_observation__mt_cad_dtv')
    derivative_mt_cad_dti = indexes.CharField(model_attr='derivative_observation__mt_cad_dti')

    derivative_mt_int = indexes.BooleanField(model_attr='derivative_observation__mt_int', faceted=True)
    derivative_mt_int_voices = indexes.CharField(model_attr='derivative_observation__mt_int_voices')
    derivative_mt_int_p6 = indexes.BooleanField(model_attr='derivative_observation__mt_int_p6', faceted=True)
    derivative_mt_int_p3 = indexes.BooleanField(model_attr='derivative_observation__mt_int_p3', faceted=True)
    derivative_mt_int_c35 = indexes.BooleanField(model_attr='derivative_observation__mt_int_c35', faceted=True)
    derivative_mt_int_c83 = indexes.BooleanField(model_attr='derivative_observation__mt_int_c83', faceted=True)
    derivative_mt_int_c65 = indexes.BooleanField(model_attr='derivative_observation__mt_int_c65', faceted=True)

    derivative_mt_fp = indexes.BooleanField(model_attr='derivative_observation__mt_fp', faceted=True)
    derivative_mt_fp_comment = indexes.CharField(model_attr='derivative_observation__mt_fp_comment')
    derivative_mt_fp_ir = indexes.BooleanField(model_attr='derivative_observation__mt_fp_ir', faceted=True)
    derivative_mt_fp_range = indexes.CharField(model_attr='derivative_observation__mt_fp_range')

    derivative_remarks = indexes.CharField(model_attr='derivative_observation__remarks', indexed=False)
    derivative_created = indexes.DateTimeField(model_attr='derivative_observation__created')
    derivative_updated = indexes.DateTimeField(model_attr='derivative_observation__updated')
    derivative_status = indexes.BooleanField(model_attr='derivative_observation__status')

    # Information about the derivative observation's CRIMPiece

    derivative_piece_id = indexes.CharField(model_attr='derivative_observation__piece__piece_id')
    derivative_title = indexes.CharField(model_attr='derivative_observation__piece__title')
    derivative_mass_title = indexes.CharField(model_attr='derivative_observation__piece__mass__title', null=True)
    derivative_composer = indexes.CharField(model_attr='derivative_observation__piece__composer__name_sort', faceted=True, null=True)
    derivative_genre = indexes.CharField(model_attr='derivative_observation__piece__genre__name', faceted=True)
    derivative_date = indexes.IntegerField(model_attr='derivative_observation__piece__date_sort', faceted=True, null=True)
    derivative_pdf_links = indexes.CharField(model_attr='derivative_observation__piece__pdf_links', null=True, indexed=False)
    derivative_mei_links = indexes.CharField(model_attr='derivative_observation__piece__mei_links', null=True, indexed=False)
    derivative_remarks = indexes.CharField(model_attr='derivative_observation__piece__remarks', null=True, indexed=False)

    def get_model(self):
        return CRIMRelationship
