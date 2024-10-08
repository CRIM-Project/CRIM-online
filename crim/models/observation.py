from django.core.cache import caches
from django.db import models
from django.db.models import JSONField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from crim.helpers.common import cache_values_to_string
from crim.models.definition import CRIMDefinition

import json


class CJObservation(models.Model):
    '''This is the new observation type created during Linh's
    summer 2021 work. It uses JSON to encode musical type using
    a CRIMDefinition object, and should be used moving forward.
    '''
    class Meta:
        app_label = 'crim'
        verbose_name = 'Observation'
        verbose_name_plural = 'Observations'

    observer = models.ForeignKey(
        'CRIMPerson',
        on_delete=models.SET_NULL,
        to_field='person_id',
        null=True,
        db_index=True,
        related_name='observations',
    )
    piece = models.ForeignKey(
        'CRIMPiece',
        on_delete=models.CASCADE,
        to_field='piece_id',
        db_index=True,
        related_name='observations',
    )

    ema = models.CharField(max_length=10000, blank=True)
    musical_type = models.CharField(max_length=128, blank=True)
    details = JSONField(blank=True, null=True)

    definition = models.ForeignKey(
        CRIMDefinition,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='observations',
        null=True
    )

    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    curated = models.BooleanField('curated', default=False)

    def id_in_brackets(self):
        return '{' + str(self.id) + '}'
    id_in_brackets.short_description = 'ID'
    id_in_brackets.admin_order_field = 'id'

    def get_absolute_url(self):
        return '/observations/{0}/'.format(self.pk)

    def __str__(self):
        return self.id_in_brackets() + f' {self.piece_id}'

    # TODO: Rework this as a pre_save signal
    # def save(self, *args, **kwargs):
    #     mtypename = str(self.musical_type).lower()
    #     allowed_types = list(self.definition.observation_definition.keys())
    #
    #     if mtypename in allowed_types:
    #         valid_sub = False
    #         allowed_subtypes = sorted(list(self.definition.observation_definition[mtypename]))
    #         string_details = json.dumps(self.details)
    #         print(dir(self))
    #         sub_dict = json.loads(string_details)
    #
    #         if allowed_subtypes == []:
    #             valid_sub = True
    #         else:
    #             curr_subtypes = sorted(list(sub_dict.keys())) if sub_dict else None
    #             if curr_subtypes:
    #                 curr_subtypes_lower = [e.lower() for e in curr_subtypes]
    #             else:
    #                 curr_subtypes_lower = None
    #
    #             if curr_subtypes_lower == allowed_subtypes:
    #                 valid_sub = True
    #
    #         if not valid_sub:
    #             print("Warning: invalid observation instance saved")
    #
    #         self.definition.save()
    #         super(CJObservation, self).save(*args, **kwargs)


class CRIMObservation(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Observation (old)'
        verbose_name_plural = 'Observations (old)'

    observer = models.ForeignKey(
        'CRIMPerson',
        on_delete=models.SET_NULL,
        to_field='person_id',
        null=True,
        db_index=True,
        related_name='old_observations',
    )

    piece = models.ForeignKey(
        'CRIMPiece',
        on_delete=models.CASCADE,
        to_field='piece_id',
        db_index=True,
        related_name='old_observations',
    )
    ema = models.TextField('EMA expression', blank=True)

    # This field provides redundant, easily accessible, human-readable
    # information about musical type. It is updated upon saving.
    musical_type = models.CharField(max_length=128, blank=True)

    mt_cf = models.BooleanField('cantus firmus', default=False)
    mt_cf_voices = models.TextField('voices (one per line)', blank=True)
    mt_cf_dur = models.BooleanField('rhythmic durations', default=False)
    mt_cf_mel = models.BooleanField('melodic intervals', default=False)

    mt_sog = models.BooleanField('soggetto', default=False)
    mt_sog_voices = models.TextField('voices (one per line)', blank=True)
    mt_sog_dur = models.BooleanField('rhythmic durations', default=False)
    mt_sog_mel = models.BooleanField('melodic intervals', default=False)
    mt_sog_ostinato = models.BooleanField('ostinato', default=False)
    mt_sog_periodic = models.BooleanField('periodic', default=False)

    mt_csog = models.BooleanField('counter-soggetto', default=False)
    mt_csog_voices = models.TextField('voices (one per line)', blank=True)
    mt_csog_dur = models.BooleanField('rhythmic durations', default=False)
    mt_csog_mel = models.BooleanField('melodic intervals', default=False)

    mt_cd = models.BooleanField('contrapuntal duo', default=False)
    mt_cd_voices = models.TextField('voices (one per line)', blank=True)

    mt_fg = models.BooleanField('fuga', default=False)
    mt_fg_voices = models.TextField('voices (one per line)', blank=True)
    mt_fg_int = models.CharField('melodic interval of entry', max_length=64, blank=True)
    mt_fg_tint = models.CharField('time interval of entry', max_length=64, blank=True)
    mt_fg_periodic = models.BooleanField('periodic', default=False)
    mt_fg_strict = models.BooleanField('strict', default=False)
    mt_fg_flexed = models.BooleanField('flexed', default=False)
    mt_fg_sequential = models.BooleanField('sequential', default=False)
    mt_fg_inverted = models.BooleanField('inverted', default=False)
    mt_fg_retrograde = models.BooleanField('retrograde', default=False)

    mt_pe = models.BooleanField('periodic entry', default=False)
    mt_pe_voices = models.TextField('voices (one per line)', blank=True)
    mt_pe_int = models.CharField('melodic interval of entry', max_length=64, blank=True)
    mt_pe_tint = models.CharField('time interval of entry', max_length=64, blank=True)
    mt_pe_strict = models.BooleanField('strict', default=False)
    mt_pe_flexed = models.BooleanField('flexed', default=False)
    mt_pe_flt = models.BooleanField('flexed, tonal', default=False)
    mt_pe_sequential = models.BooleanField('sequential', default=False)
    mt_pe_added = models.BooleanField('added', default=False)
    mt_pe_invertible = models.BooleanField('invertible', default=False)

    mt_id = models.BooleanField('imitative duo', default=False)
    mt_id_voices = models.TextField('voices (one per line)', blank=True)
    mt_id_int = models.CharField('melodic interval of entry', max_length=64, blank=True)
    mt_id_tint = models.CharField('time interval of entry', max_length=64, blank=True)
    mt_id_strict = models.BooleanField('strict', default=False)
    mt_id_flexed = models.BooleanField('flexed', default=False)
    mt_id_flt = models.BooleanField('flexed, tonal', default=False)
    mt_id_invertible = models.BooleanField('invertible', default=False)

    mt_nid = models.BooleanField('non-imitative duo', default=False)
    mt_nid_voices = models.TextField('voices (one per line)', blank=True)
    mt_nid_int = models.CharField('melodic interval of entry', max_length=64, blank=True)
    mt_nid_tint = models.CharField('time interval of entry', max_length=64, blank=True)
    mt_nid_strict = models.BooleanField('strict', default=False)
    mt_nid_flexed = models.BooleanField('flexed', default=False)
    mt_nid_flt = models.BooleanField('flexed, tonal', default=False)
    mt_nid_sequential = models.BooleanField('sequential', default=False)
    mt_nid_invertible = models.BooleanField('invertible', default=False)

    mt_hr = models.BooleanField('homorhythm', default=False)
    mt_hr_voices = models.TextField('voices (one per line)', blank=True)
    mt_hr_simple = models.BooleanField('simple', default=False)
    mt_hr_staggered = models.BooleanField('staggered', default=False)
    mt_hr_sequential = models.BooleanField('sequential', default=False)
    mt_hr_fauxbourdon = models.BooleanField('fauxbourdon', default=False)

    mt_cad = models.BooleanField('cadence', default=False)
    mt_cad_cantizans = models.TextField('cantizans', blank=True)
    mt_cad_tenorizans = models.TextField('tenorizans', blank=True)
    mt_cad_type = models.CharField('type (authentic, phrygian, plagal)', max_length=32, blank=True)
    mt_cad_tone = models.CharField('tone (e.g. D, A, b; indicate flat tone with lowercase letter)', max_length=16, blank=True)
    mt_cad_dtv = models.CharField('dovetail voice', max_length=64, blank=True)
    mt_cad_dti = models.CharField('dovetail interval', max_length=64, blank=True)

    mt_int = models.BooleanField('interval pattern', default=False)
    mt_int_voices = models.TextField('voices (one per line)', blank=True)
    mt_int_p6 = models.BooleanField('parallel 6', default=False)
    mt_int_p3 = models.BooleanField('parallel 3 (or 10)', default=False)
    mt_int_c35 = models.BooleanField('chained 3 and 5', default=False)
    mt_int_c83 = models.BooleanField('chained 8 and 3', default=False)
    mt_int_c65 = models.BooleanField('chained 6 and 5', default=False)

    mt_fp = models.BooleanField('form and process', default=False)
    mt_fp_ir = models.BooleanField('internal repetition', default=False)
    mt_fp_range = models.CharField('range', max_length=32, blank=True)
    mt_fp_comment = models.TextField('comment', blank=True)

    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    curated = models.BooleanField('curated', default=False)

    def id_in_brackets(self):
        return '<' + str(self.id) + '>'
    id_in_brackets.short_description = 'ID'
    id_in_brackets.admin_order_field = 'id'

    def get_absolute_url(self):
        return '/observations-old/{0}/'.format(self.pk)

    def __str__(self):
        return '<{0}> {1}'.format(self.id, self.piece_id)

    def save(self):
        # Set the parent relationship type field to true if any of the subtypes are
        self.mt_cf = bool(self.mt_cf_voices or self.mt_cf_dur or self.mt_cf_mel)
        self.mt_sog = bool(self.mt_sog_voices or self.mt_sog_dur or self.mt_sog_mel or self.mt_sog_ostinato or self.mt_sog_periodic)
        self.mt_csog = bool(self.mt_csog_voices or self.mt_csog_dur or self.mt_csog_mel)
        self.mt_cd = bool(self.mt_cd_voices)
        self.mt_fg = bool(self.mt_fg_voices or self.mt_fg_periodic or self.mt_fg_strict or self.mt_fg_flexed or self.mt_fg_sequential or self.mt_fg_inverted or self.mt_fg_retrograde or self.mt_fg_int or self.mt_fg_tint)
        self.mt_id = bool(self.mt_id_voices or self.mt_id_strict or self.mt_id_flexed or self.mt_id_flt or self.mt_id_invertible or self.mt_id_int or self.mt_id_tint)
        self.mt_pe = bool(self.mt_pe_voices or self.mt_pe_strict or self.mt_pe_flexed or self.mt_pe_flt or self.mt_pe_sequential or self.mt_pe_added or self.mt_pe_invertible or self.mt_pe_int or self.mt_pe_tint)
        self.mt_nid = bool(self.mt_nid_voices or self.mt_nid_strict or self.mt_nid_flexed or self.mt_nid_flt or self.mt_nid_sequential or self.mt_nid_invertible or self.mt_nid_int or self.mt_nid_tint)
        self.mt_hr = bool(self.mt_hr_voices or self.mt_hr_simple or self.mt_hr_staggered or self.mt_hr_sequential or self.mt_hr_fauxbourdon)
        self.mt_cad = bool(self.mt_cad_cantizans or self.mt_cad_tenorizans or self.mt_cad_type or self.mt_cad_tone or self.mt_cad_dtv or self.mt_cad_dti)
        self.mt_int = bool(self.mt_int_voices or self.mt_int_p6 or self.mt_int_p3 or self.mt_int_c35 or self.mt_int_c83 or self.mt_int_c65)
        self.mt_fp = bool(self.mt_fp_ir or self.mt_fp_range or self.mt_fp_comment)

        # Fill out the human-readable musical type field.
        # There's only SUPPOSED to be one, but some data are dirty, so we
        # want to display these gracefully.
        musical_type_list = []
        if self.mt_cf:
            musical_type_list.append('Cantus firmus')
        if self.mt_sog:
            musical_type_list.append('Soggetto')
        if self.mt_csog:
            musical_type_list.append('Counter-soggetto')
        if self.mt_cd:
            musical_type_list.append('Contrapuntal duo')
        if self.mt_fg:
            musical_type_list.append('Fuga')
        if self.mt_pe:
            musical_type_list.append('Periodic entry')
        if self.mt_id:
            musical_type_list.append('Imitative duo')
        if self.mt_nid:
            musical_type_list.append('Non-imitative duo')
        if self.mt_hr:
            musical_type_list.append('Homorhythm')
        if self.mt_cad:
            musical_type_list.append('Cadence')
        if self.mt_int:
            musical_type_list.append('Interval patterns')
        if self.mt_fp:
            musical_type_list.append('Form and process')
        self.musical_type = ', '.join(musical_type_list)

        # Finalize changes
        super().save()


# @receiver(post_save, sender=CRIMObservation)
# def update_observation_cache(sender, instance, created, **kwargs):
#    if not kwargs.get('raw', True):  # So that this does not run when importing fixture
#        from crim.views.observation import render_observation
#        print('Caching <{}>'.format(instance.id))
#        render_observation(instance.id, instance.piece.piece_id, instance.ema, None)
#        # Delete page caches, which might have changed. Don't want to take the time
#        # to cache them all right now; use a management command for that.
#        for i in range(30):
#            caches['observations'].delete(cache_values_to_string(
#                    instance.id,
#                    i+1,
#                ))


# @receiver(post_delete, sender=CRIMObservation)
# def delete_observation_cache(sender, instance, **kwargs):
#     from django.core.cache import caches
#     print('Deleting cache for <{}>'.format(instance.id))
#     caches['observations'].delete(cache_values_to_string(
#             instance.id,
#             None,
#         ))
#     for i in range(30):
#         caches['observations'].delete(cache_values_to_string(
#                 instance.id,
#                 i+1,
#             ))
