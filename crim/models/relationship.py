from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class CRIMRelationship(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Relationship'
        verbose_name_plural = 'Relationships'

    observer = models.ForeignKey(
        'CRIMPerson',
        on_delete=models.SET_NULL,
        to_field='person_id',
        null=True,
        db_index=True,
        related_name='relationships',
    )

    model_observation = models.ForeignKey(
        'CRIMObservation',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='observations_as_model',
    )
    derivative_observation = models.ForeignKey(
        'CRIMObservation',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='observations_as_derivative',
    )

    rt_q = models.BooleanField('quotation', default=False)
    rt_q_x = models.BooleanField('exact', default=False)
    rt_q_monnayage = models.BooleanField('monnayage', default=False)

    rt_tm = models.BooleanField('mechanical transformation', default=False)
    rt_tm_snd = models.BooleanField('sounding in different voice(s)', default=False)
    rt_tm_minv = models.BooleanField('melodically inverted', default=False)
    rt_tm_retrograde = models.BooleanField('retrograde', default=False)
    rt_tm_ms = models.BooleanField('metrically shifted', default=False)
    rt_tm_transposed = models.BooleanField('transposed', default=False)
    rt_tm_invertible = models.BooleanField('double or invertible counterpoint', default=False)

    rt_tnm = models.BooleanField('non-mechanical transformation', default=False)
    rt_tnm_embellished = models.BooleanField('embellished', default=False)
    rt_tnm_reduced = models.BooleanField('reduced', default=False)
    rt_tnm_amplified = models.BooleanField('amplified', default=False)
    rt_tnm_truncated = models.BooleanField('truncated', default=False)
    rt_tnm_ncs = models.BooleanField('new counter-subject', default=False)
    rt_tnm_ocs = models.BooleanField('old counter-subject shifted', default=False)
    rt_tnm_ocst = models.BooleanField('old counter-subject transposed', default=False)
    rt_tnm_nc = models.BooleanField('new combination', default=False)

    rt_nm = models.BooleanField('new material', default=False)
    rt_om = models.BooleanField('omission', default=False)

    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField('status', default=True)

    def id_in_brackets(self):
        return '<R' + str(self.id) + '>'
    id_in_brackets.short_description = 'ID'
    id_in_brackets.admin_order_field = 'id'

    def get_absolute_url(self):
        return '/relationship/{0}/'.format(self.pk)

    def __str__(self):
        return '<R{0}> {1}, {2}'.format(
            self.id,
            self.model_observation.piece_id,
            self.derivative_observation.piece_id
        )

    def save(self, *args, **kwargs):
        # Set the parent relationship type field to true if any of the subtypes are
        if self.rt_q_x or self.rt_q_monnayage:
            self.rt_q = True
        if (self.rt_tm_snd or self.rt_tm_minv or self.rt_tm_retrograde or
                self.rt_tm_ms or self.rt_tm_transposed or self.rt_tm_invertible):
            self.rt_tm = True
        if (self.rt_tnm_embellished or self.rt_tnm_reduced or self.rt_tnm_amplified or
            self.rt_tnm_truncated or self.rt_tnm_ncs or self.rt_tnm_ocs or
                self.rt_tnm_ocst or self.rt_tnm_nc):
            self.rt_tnm = True
        # Finalize changes
        super().save()


@receiver(post_save, sender=CRIMRelationship)
def solr_index(sender, instance, created, **kwargs):
    print('Indexing in Solr')
    from django.conf import settings
    import solr

    solrconn = solr.SolrConnection(settings.SOLR_SERVER)
    record = solrconn.query("id:{0}".format(instance.id))
    if record:
        # the record already exists, so we'll remove it first.
        print("Deleting {}".format(record.results[0]['id']))
        solrconn.delete(record.results[0]['id'])

    # Don't index if this relationship needs review!
    if not instance.status:
        return
    # The suffixes are for automatic creation of the schema using
    # the correct types -- see http://yonik.com/solr-tutorial/
    d = {
        'type': 'crim_relationship',
        'id': instance.id,
        'observer_s': instance.observer.name,

        # Information about the relationship type

        'rt_q_b': instance.rt_q,
        'rt_q_x_b': instance.rt_q_x,
        'rt_q_monnayage_b': instance.rt_q_monnayage,

        'rt_tm_b': instance.rt_tm,
        'rt_tm_snd_b': instance.rt_tm_snd,
        'rt_tm_minv_b': instance.rt_tm_minv,
        'rt_tm_retrograde_b': instance.rt_tm_retrograde,
        'rt_tm_ms_b': instance.rt_tm_ms,
        'rt_tm_transposed_b': instance.rt_tm_transposed,
        'rt_tm_invertible_b': instance.rt_tm_invertible,

        'rt_tnm_b': instance.rt_tnm,
        'rt_tnm_embellished_b': instance.rt_tnm_embellished,
        'rt_tnm_reduced_b': instance.rt_tnm_reduced,
        'rt_tnm_amplified_b': instance.rt_tnm_amplified,
        'rt_tnm_truncated_b': instance.rt_tnm_truncated,
        'rt_tnm_ncs_b': instance.rt_tnm_ncs,
        'rt_tnm_ocs_b': instance.rt_tnm_ocs,
        'rt_tnm_ocst_b': instance.rt_tnm_ocst,
        'rt_tnm_nc_b': instance.rt_tnm_nc,

        'rt_nm_b': instance.rt_nm,
        'rt_om_b': instance.rt_om,

        'remarks_t': instance.remarks,
        'created_dt': instance.created,
        'updated_dt': instance.updated,
        'status_b': instance.status,

        # Information about the model CRIMObservation

        'model_observer_s': instance.model_observation.observer.name,
        'model_ema_s': instance.model_observation.ema,

        'model_mt_cf_b': instance.model_observation.mt_cf,
        'model_mt_cf_voices_ss': instance.model_observation.mt_cf_voices.split('\n'),
        'model_mt_cf_dur_b': instance.model_observation.mt_cf_dur,
        'model_mt_cf_mel_b': instance.model_observation.mt_cf_mel,

        'model_mt_sog_b': instance.model_observation.mt_sog,
        'model_mt_sog_voices_ss': instance.model_observation.mt_sog_voices.split('\n'),
        'model_mt_sog_dur_b': instance.model_observation.mt_sog_dur,
        'model_mt_sog_mel_b': instance.model_observation.mt_sog_mel,
        'model_mt_sog_ostinato_b': instance.model_observation.mt_sog_ostinato,
        'model_mt_sog_periodic_b': instance.model_observation.mt_sog_periodic,

        'model_mt_csog_b': instance.model_observation.mt_csog,
        'model_mt_csog_voices_ss': instance.model_observation.mt_csog_voices.split('\n'),
        'model_mt_csog_dur_b': instance.model_observation.mt_csog_dur,
        'model_mt_csog_mel_b': instance.model_observation.mt_csog_mel,

        'model_mt_cd_b': instance.model_observation.mt_cd,
        'model_mt_cd_voices_ss': instance.model_observation.mt_cd_voices.split('\n'),

        'model_mt_fg_b': instance.model_observation.mt_fg,
        'model_mt_fg_voices_ss': instance.model_observation.mt_fg_voices.split('\n'),
        'model_mt_fg_periodic_b': instance.model_observation.mt_fg_periodic,
        'model_mt_fg_strict_b': instance.model_observation.mt_fg_strict,
        'model_mt_fg_flexed_b': instance.model_observation.mt_fg_flexed,
        'model_mt_fg_sequential_b': instance.model_observation.mt_fg_sequential,
        'model_mt_fg_inverted_b': instance.model_observation.mt_fg_inverted,
        'model_mt_fg_retrograde_b': instance.model_observation.mt_fg_retrograde,
        'model_mt_fg_int_s': instance.model_observation.mt_fg_int,
        'model_mt_fg_tint_s': instance.model_observation.mt_fg_tint,

        'model_mt_id_b': instance.model_observation.mt_id,
        'model_mt_id_voices_ss': instance.model_observation.mt_id_voices.split('\n'),
        'model_mt_id_strict_b': instance.model_observation.mt_id_strict,
        'model_mt_id_flexed_b': instance.model_observation.mt_id_flexed,
        'model_mt_id_flt_b': instance.model_observation.mt_id_flt,
        'model_mt_id_invertible_b': instance.model_observation.mt_id_invertible,
        'model_mt_id_int_s': instance.model_observation.mt_id_int,
        'model_mt_id_tint_s': instance.model_observation.mt_id_tint,

        'model_mt_pe_b': instance.model_observation.mt_pe,
        'model_mt_pe_voices_ss': instance.model_observation.mt_pe_voices.split('\n'),
        'model_mt_pe_strict_b': instance.model_observation.mt_pe_strict,
        'model_mt_pe_flexed_b': instance.model_observation.mt_pe_flexed,
        'model_mt_pe_flt_b': instance.model_observation.mt_pe_flt,
        'model_mt_pe_sequential_b': instance.model_observation.mt_pe_sequential,
        'model_mt_pe_added_b': instance.model_observation.mt_pe_added,
        'model_mt_pe_invertible_b': instance.model_observation.mt_pe_invertible,
        'model_mt_pe_int_s': instance.model_observation.mt_pe_int,
        'model_mt_pe_tint_s': instance.model_observation.mt_pe_tint,

        'model_mt_nid_b': instance.model_observation.mt_nid,
        'model_mt_nid_voices_ss': instance.model_observation.mt_nid_voices.split('\n'),
        'model_mt_nid_strict_b': instance.model_observation.mt_nid_strict,
        'model_mt_nid_flexed_b': instance.model_observation.mt_nid_flexed,
        'model_mt_nid_flt_b': instance.model_observation.mt_nid_flt,
        'model_mt_nid_sequential_b': instance.model_observation.mt_nid_sequential,
        'model_mt_nid_invertible_b': instance.model_observation.mt_nid_invertible,
        'model_mt_nid_int_s': instance.model_observation.mt_nid_int,
        'model_mt_nid_tint_s': instance.model_observation.mt_nid_tint,

        'model_mt_hr_b': instance.model_observation.mt_hr,
        'model_mt_hr_voices_ss': instance.model_observation.mt_hr_voices.split('\n'),
        'model_mt_hr_simple_b': instance.model_observation.mt_hr_simple,
        'model_mt_hr_staggered_b': instance.model_observation.mt_hr_staggered,
        'model_mt_hr_sequential_b': instance.model_observation.mt_hr_sequential,
        'model_mt_hr_fauxbourdon_b': instance.model_observation.mt_hr_fauxbourdon,

        'model_mt_cad_b': instance.model_observation.mt_cad,
        'model_mt_cad_cantizans_s': instance.model_observation.mt_cad_cantizans,
        'model_mt_cad_tenorizans_s': instance.model_observation.mt_cad_tenorizans,
        'model_mt_cad_authentic_b': instance.model_observation.mt_cad_authentic,
        'model_mt_cad_phrygian_b': instance.model_observation.mt_cad_phrygian,
        'model_mt_cad_plagal_b': instance.model_observation.mt_cad_plagal,
        'model_mt_cad_tone_s': instance.model_observation.mt_cad_tone,
        'model_mt_cad_dtv_s': instance.model_observation.mt_cad_dtv,
        'model_mt_cad_dti_s': instance.model_observation.mt_cad_dti,

        'model_mt_int_b': instance.model_observation.mt_int,
        'model_mt_int_voices_ss': instance.model_observation.mt_int_voices.split('\n'),
        'model_mt_int_p6_b': instance.model_observation.mt_int_p6,
        'model_mt_int_p3_b': instance.model_observation.mt_int_p3,
        'model_mt_int_c35_b': instance.model_observation.mt_int_c35,
        'model_mt_int_c83_b': instance.model_observation.mt_int_c83,
        'model_mt_int_c65_b': instance.model_observation.mt_int_c65,

        'model_mt_fp_b': instance.model_observation.mt_fp,
        'model_mt_fp_comment_t': instance.model_observation.mt_fp_comment,
        'model_mt_fp_ir_b': instance.model_observation.mt_fp_ir,
        'model_mt_fp_range_s': instance.model_observation.mt_fp_range,

        'model_remarks_t': instance.model_observation.remarks,
        'model_created_dt': instance.model_observation.created,
        'model_updated_dt': instance.model_observation.updated,
        'model_status_b': instance.model_observation.status,

        # Information about the model observation's CRIMPiece

        'model_piece_id_s': instance.model_observation.piece.piece_id,
        'model_title_s': instance.model_observation.piece.title,
        'model_mass_s': instance.model_observation.piece.mass.title if instance.model_observation.piece.mass else None,
        'model_composer_s': instance.model_observation.piece.composer.name,
        'model_genre_s': instance.model_observation.piece.genre,
        'model_date_i': instance.model_observation.piece.date_sort,
        'model_pdf_links_ss': instance.model_observation.piece.pdf_links.split('\n'),
        'model_mei_links_ss': instance.model_observation.piece.mei_links.split('\n'),
        'model_remarks_t': instance.model_observation.piece.remarks,

        # Information about the derivative CRIMObservation

        'derivative_observer_s': instance.derivative_observation.observer.name,
        'derivative_ema_s': instance.derivative_observation.ema,

        'derivative_mt_cf_b': instance.derivative_observation.mt_cf,
        'derivative_mt_cf_voices_ss': instance.derivative_observation.mt_cf_voices.split('\n'),
        'derivative_mt_cf_dur_b': instance.derivative_observation.mt_cf_dur,
        'derivative_mt_cf_mel_b': instance.derivative_observation.mt_cf_mel,

        'derivative_mt_sog_b': instance.derivative_observation.mt_sog,
        'derivative_mt_sog_voices_ss': instance.derivative_observation.mt_sog_voices.split('\n'),
        'derivative_mt_sog_dur_b': instance.derivative_observation.mt_sog_dur,
        'derivative_mt_sog_mel_b': instance.derivative_observation.mt_sog_mel,
        'derivative_mt_sog_ostinato_b': instance.derivative_observation.mt_sog_ostinato,
        'derivative_mt_sog_periodic_b': instance.derivative_observation.mt_sog_periodic,

        'derivative_mt_csog_b': instance.derivative_observation.mt_csog,
        'derivative_mt_csog_voices_ss': instance.derivative_observation.mt_csog_voices.split('\n'),
        'derivative_mt_csog_dur_b': instance.derivative_observation.mt_csog_dur,
        'derivative_mt_csog_mel_b': instance.derivative_observation.mt_csog_mel,

        'derivative_mt_cd_b': instance.derivative_observation.mt_cd,
        'derivative_mt_cd_voices_ss': instance.derivative_observation.mt_cd_voices.split('\n'),

        'derivative_mt_fg_b': instance.derivative_observation.mt_fg,
        'derivative_mt_fg_voices_ss': instance.derivative_observation.mt_fg_voices.split('\n'),
        'derivative_mt_fg_periodic_b': instance.derivative_observation.mt_fg_periodic,
        'derivative_mt_fg_strict_b': instance.derivative_observation.mt_fg_strict,
        'derivative_mt_fg_flexed_b': instance.derivative_observation.mt_fg_flexed,
        'derivative_mt_fg_sequential_b': instance.derivative_observation.mt_fg_sequential,
        'derivative_mt_fg_inverted_b': instance.derivative_observation.mt_fg_inverted,
        'derivative_mt_fg_retrograde_b': instance.derivative_observation.mt_fg_retrograde,
        'derivative_mt_fg_int_s': instance.derivative_observation.mt_fg_int,
        'derivative_mt_fg_tint_s': instance.derivative_observation.mt_fg_tint,

        'derivative_mt_id_b': instance.derivative_observation.mt_id,
        'derivative_mt_id_voices_ss': instance.derivative_observation.mt_id_voices.split('\n'),
        'derivative_mt_id_strict_b': instance.derivative_observation.mt_id_strict,
        'derivative_mt_id_flexed_b': instance.derivative_observation.mt_id_flexed,
        'derivative_mt_id_flt_b': instance.derivative_observation.mt_id_flt,
        'derivative_mt_id_invertible_b': instance.derivative_observation.mt_id_invertible,
        'derivative_mt_id_int_s': instance.derivative_observation.mt_id_int,
        'derivative_mt_id_tint_s': instance.derivative_observation.mt_id_tint,

        'derivative_mt_pe_b': instance.derivative_observation.mt_pe,
        'derivative_mt_pe_voices_ss': instance.derivative_observation.mt_pe_voices.split('\n'),
        'derivative_mt_pe_strict_b': instance.derivative_observation.mt_pe_strict,
        'derivative_mt_pe_flexed_b': instance.derivative_observation.mt_pe_flexed,
        'derivative_mt_pe_flt_b': instance.derivative_observation.mt_pe_flt,
        'derivative_mt_pe_sequential_b': instance.derivative_observation.mt_pe_sequential,
        'derivative_mt_pe_added_b': instance.derivative_observation.mt_pe_added,
        'derivative_mt_pe_invertible_b': instance.derivative_observation.mt_pe_invertible,
        'derivative_mt_pe_int_s': instance.derivative_observation.mt_pe_int,
        'derivative_mt_pe_tint_s': instance.derivative_observation.mt_pe_tint,

        'derivative_mt_nid_b': instance.derivative_observation.mt_nid,
        'derivative_mt_nid_voices_ss': instance.derivative_observation.mt_nid_voices.split('\n'),
        'derivative_mt_nid_strict_b': instance.derivative_observation.mt_nid_strict,
        'derivative_mt_nid_flexed_b': instance.derivative_observation.mt_nid_flexed,
        'derivative_mt_nid_flt_b': instance.derivative_observation.mt_nid_flt,
        'derivative_mt_nid_sequential_b': instance.derivative_observation.mt_nid_sequential,
        'derivative_mt_nid_invertible_b': instance.derivative_observation.mt_nid_invertible,
        'derivative_mt_nid_int_s': instance.derivative_observation.mt_nid_int,
        'derivative_mt_nid_tint_s': instance.derivative_observation.mt_nid_tint,

        'derivative_mt_hr_b': instance.derivative_observation.mt_hr,
        'derivative_mt_hr_voices_ss': instance.derivative_observation.mt_hr_voices.split('\n'),
        'derivative_mt_hr_simple_b': instance.derivative_observation.mt_hr_simple,
        'derivative_mt_hr_staggered_b': instance.derivative_observation.mt_hr_staggered,
        'derivative_mt_hr_sequential_b': instance.derivative_observation.mt_hr_sequential,
        'derivative_mt_hr_fauxbourdon_b': instance.derivative_observation.mt_hr_fauxbourdon,

        'derivative_mt_cad_b': instance.derivative_observation.mt_cad,
        'derivative_mt_cad_cantizans_s': instance.derivative_observation.mt_cad_cantizans,
        'derivative_mt_cad_tenorizans_s': instance.derivative_observation.mt_cad_tenorizans,
        'derivative_mt_cad_authentic_b': instance.derivative_observation.mt_cad_authentic,
        'derivative_mt_cad_phrygian_b': instance.derivative_observation.mt_cad_phrygian,
        'derivative_mt_cad_plagal_b': instance.derivative_observation.mt_cad_plagal,
        'derivative_mt_cad_tone_s': instance.derivative_observation.mt_cad_tone,
        'derivative_mt_cad_dtv_s': instance.derivative_observation.mt_cad_dtv,
        'derivative_mt_cad_dti_s': instance.derivative_observation.mt_cad_dti,

        'derivative_mt_int_b': instance.derivative_observation.mt_int,
        'derivative_mt_int_voices_ss': instance.derivative_observation.mt_int_voices.split('\n'),
        'derivative_mt_int_p6_b': instance.derivative_observation.mt_int_p6,
        'derivative_mt_int_p3_b': instance.derivative_observation.mt_int_p3,
        'derivative_mt_int_c35_b': instance.derivative_observation.mt_int_c35,
        'derivative_mt_int_c83_b': instance.derivative_observation.mt_int_c83,
        'derivative_mt_int_c65_b': instance.derivative_observation.mt_int_c65,

        'derivative_mt_fp_b': instance.derivative_observation.mt_fp,
        'derivative_mt_fp_comment_t': instance.derivative_observation.mt_fp_comment,
        'derivative_mt_fp_ir_b': instance.derivative_observation.mt_fp_ir,
        'derivative_mt_fp_range_s': instance.derivative_observation.mt_fp_range,

        'derivative_remarks_t': instance.derivative_observation.remarks,
        'derivative_created_dt': instance.derivative_observation.created,
        'derivative_updated_dt': instance.derivative_observation.updated,
        'derivative_status_b': instance.derivative_observation.status,

        # Information about the derivative observation's CRIMPiece

        'derivative_piece_id_s': instance.derivative_observation.piece.piece_id,
        'derivative_title_s': instance.derivative_observation.piece.title,
        'derivative_mass_s': instance.derivative_observation.piece.mass.title if instance.derivative_observation.piece.mass else None,
        'derivative_composer_s': instance.derivative_observation.piece.composer.name,
        'derivative_genre_s': instance.derivative_observation.piece.genre,
        'derivative_date_i': instance.derivative_observation.piece.date_sort,
        'derivative_pdf_links_ss': instance.derivative_observation.piece.pdf_links.split('\n'),
        'derivative_mei_links_ss': instance.derivative_observation.piece.mei_links.split('\n'),
        'derivative_remarks_t': instance.derivative_observation.piece.remarks,
    }
    solrconn.add(**d)
    solrconn.commit()


@receiver(post_delete, sender=CRIMRelationship)
def solr_delete(sender, instance, **kwargs):
    from django.conf import settings
    import solr

    solrconn = solr.SolrConnection(settings.SOLR_SERVER)
    record = solrconn.query("id:{0}".format(instance.id))
    if record:
        # the record already exists, so we'll remove it first.
        print("Deleting ".format(record.results[0]['id']))
        solrconn.delete(record.results[0]['id'])
