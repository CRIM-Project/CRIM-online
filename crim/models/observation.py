from django.db import models


class CRIMObservation(models.Model):
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
    ema = models.TextField('EMA expression', blank=True)

    # This field provides redundant, easily accessible, human-readable
    # information about musical type. It is updated upon saving.
    musical_type = models.CharField(max_length=64, blank=True)

    mt_cf = models.BooleanField('cantus firmus', default=False)
    mt_cf_voices = models.TextField('voices (one per line)', blank=True)
    mt_cf_dur = models.BooleanField('durations only', default=False)
    mt_cf_mel = models.BooleanField('intervals only', default=False)

    mt_sog = models.BooleanField('soggetto', default=False)
    mt_sog_voices = models.TextField('voices (one per line)', blank=True)
    mt_sog_dur = models.BooleanField('durations only', default=False)
    mt_sog_mel = models.BooleanField('intervals only', default=False)
    mt_sog_ostinato = models.BooleanField('ostinato', default=False)
    mt_sog_periodic = models.BooleanField('periodic', default=False)

    mt_csog = models.BooleanField('counter-soggetto', default=False)
    mt_csog_voices = models.TextField('voices (one per line)', blank=True)
    mt_csog_dur = models.BooleanField('durations only', default=False)
    mt_csog_mel = models.BooleanField('intervals only', default=False)

    mt_cd = models.BooleanField('contrapuntal duo', default=False)
    mt_cd_voices = models.TextField('voices (one per line)', blank=True)

    mt_fg = models.BooleanField('fuga', default=False)
    mt_fg_voices = models.TextField('voices (one per line)', blank=True)
    mt_fg_periodic = models.BooleanField('periodic', default=False)
    mt_fg_strict = models.BooleanField('strict', default=False)
    mt_fg_flexed = models.BooleanField('flexed', default=False)
    mt_fg_sequential = models.BooleanField('sequential', default=False)
    mt_fg_inverted = models.BooleanField('inverted', default=False)
    mt_fg_retrograde = models.BooleanField('retrograde', default=False)
    mt_fg_int = models.CharField('melodic interval of entry', max_length=32, blank=True)
    mt_fg_tint = models.CharField('time interval of entry', max_length=32, blank=True)

    mt_pe = models.BooleanField('periodic entry', default=False)
    mt_pe_voices = models.TextField('voices (one per line)', blank=True)
    mt_pe_strict = models.BooleanField('strict', default=False)
    mt_pe_flexed = models.BooleanField('flexed', default=False)
    mt_pe_flt = models.BooleanField('flexed, tonal', default=False)
    mt_pe_sequential = models.BooleanField('sequential', default=False)
    mt_pe_added = models.BooleanField('added', default=False)
    mt_pe_invertible = models.BooleanField('invertible', default=False)
    mt_pe_int = models.CharField('melodic interval of entry', max_length=32, blank=True)
    mt_pe_tint = models.CharField('time interval of entry', max_length=32, blank=True)

    mt_id = models.BooleanField('imitative duo', default=False)
    mt_id_voices = models.TextField('voices (one per line)', blank=True)
    mt_id_strict = models.BooleanField('strict', default=False)
    mt_id_flexed = models.BooleanField('flexed', default=False)
    mt_id_flt = models.BooleanField('flexed, tonal', default=False)
    mt_id_invertible = models.BooleanField('invertible', default=False)
    mt_id_int = models.CharField('melodic interval of entry', max_length=32, blank=True)
    mt_id_tint = models.CharField('time interval of entry', max_length=32, blank=True)

    mt_nid = models.BooleanField('non-imitative duo', default=False)
    mt_nid_voices = models.TextField('voices (one per line)', blank=True)
    mt_nid_strict = models.BooleanField('strict', default=False)
    mt_nid_flexed = models.BooleanField('flexed', default=False)
    mt_nid_flt = models.BooleanField('flexed, tonal', default=False)
    mt_nid_sequential = models.BooleanField('sequential', default=False)
    mt_nid_invertible = models.BooleanField('invertible', default=False)
    mt_nid_int = models.CharField('melodic interval of entry', max_length=32, blank=True)
    mt_nid_tint = models.CharField('time interval of entry', max_length=32, blank=True)

    mt_hr = models.BooleanField('homorhythm', default=False)
    mt_hr_voices = models.TextField('voices (one per line)', blank=True)
    mt_hr_simple = models.BooleanField('simple', default=False)
    mt_hr_staggered = models.BooleanField('staggered', default=False)
    mt_hr_sequential = models.BooleanField('sequential', default=False)
    mt_hr_fauxbourdon = models.BooleanField('fauxbourdon', default=False)

    mt_cad = models.BooleanField('cadence', default=False)
    mt_cad_cantizans = models.TextField('cantizans', blank=True)
    mt_cad_tenorizans = models.TextField('tenorizans', blank=True)
    mt_cad_type = models.CharField('type', max_length=32, blank=True)
    mt_cad_tone = models.CharField('tone', max_length=16, blank=True)
    mt_cad_dtv = models.CharField('dovetail voice', max_length=32, blank=True)
    mt_cad_dti = models.CharField('dovetail interval', max_length=32, blank=True)

    mt_int = models.BooleanField('interval pattern', default=False)
    mt_int_voices = models.TextField('voices (one per line)', blank=True)
    mt_int_p6 = models.BooleanField('parallel 6', default=False)
    mt_int_p3 = models.BooleanField('parallel 3 (or 10)', default=False)
    mt_int_c35 = models.BooleanField('chained 3 and 5', default=False)
    mt_int_c83 = models.BooleanField('chained 8 and 3', default=False)
    mt_int_c65 = models.BooleanField('chained 6 and 5', default=False)

    mt_fp = models.BooleanField('form and process', default=False)
    mt_fp_comment = models.TextField('comment', blank=True)
    mt_fp_ir = models.BooleanField('internal repetition', default=False)
    mt_fp_range = models.CharField('range', max_length=16, blank=True)

    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField('status', default=True)

    def id_in_brackets(self):
        return '<' + str(self.id) + '>'
    id_in_brackets.short_description = 'ID'
    id_in_brackets.admin_order_field = 'id'

    def get_absolute_url(self):
        return '/observation/{0}/'.format(self.pk)

    def save(self):
        # Set the parent relationship type field to true if any of the subtypes are
        if self.mt_cf_voices or self.mt_cf_dur or self.mt_cf_mel:
            self.mt_cf = True
        if self.mt_sog_voices or self.mt_sog_dur or self.mt_sog_mel or self.mt_sog_ostinato or self.mt_sog_periodic:
            self.mt_sog = True
        if self.mt_csog_voices or self.mt_csog_dur or self.mt_csog_mel:
            self.mt_csog = True
        if self.mt_fg_voices or self.mt_fg_periodic or self.mt_fg_strict or self.mt_fg_flexed or self.mt_fg_sequential or self.mt_fg_inverted or self.mt_fg_retrograde or self.mt_fg_int or self.mt_fg_tint:
            self.mt_fg = True
        if self.mt_id_voices or self.mt_id_strict or self.mt_id_flexed or self.mt_id_flt or self.mt_id_invertible or self.mt_id_int or self.mt_id_tint:
            self.mt_id = True
        if self.mt_pe_voices or self.mt_pe_strict or self.mt_pe_flexed or self.mt_pe_flt or self.mt_pe_sequential or self.mt_pe_added or self.mt_pe_invertible or self.mt_pe_int or self.mt_pe_tint:
            self.mt_pe = True
        if self.mt_nid_voices or self.mt_nid_strict or self.mt_nid_flexed or self.mt_nid_flt or self.mt_nid_sequential or self.mt_nid_invertible or self.mt_nid_int or self.mt_nid_tint:
            self.mt_nid = True
        if self.mt_hr_voices or self.mt_hr_simple or self.mt_hr_staggered or self.mt_hr_sequential or self.mt_hr_fauxbourdon:
            self.mt_hr = True
        if self.mt_cad_cantizans or self.mt_cad_tenorizans or self.mt_cad_type or self.mt_cad_tone or self.mt_cad_dtv or self.mt_cad_dti:
            self.mt_cad = True
        if self.mt_int_voices or self.mt_int_p6 or self.mt_int_p3 or self.mt_int_c35 or self.mt_int_c83 or self.mt_int_c65:
            self.mt_int = True
        if self.mt_fp_comment or self.mt_fp_ir or self.mt_fp_range:
            self.mt_fp = True

        # Fill out the human-readable musical type field
        if self.mt_cf:
            self.musical_type = 'Cantus firmus'
        elif self.mt_sog:
            self.musical_type = 'Soggetto'
        elif self.mt_csog:
            self.musical_type = 'Counter-soggetto'
        elif self.mt_cd:
            self.musical_type = 'Contrapuntal duo'
        elif self.mt_fg:
            self.musical_type = 'Fuga'
        elif self.mt_pe:
            self.musical_type = 'Periodic entry'
        elif self.mt_id:
            self.musical_type = 'Imitative duo'
        elif self.mt_nid:
            self.musical_type = 'Non-imitative duo'
        elif self.mt_hr:
            self.musical_type = 'Homorhythm'
        elif self.mt_cad:
            self.musical_type = 'Cadence'
        elif self.mt_int:
            self.musical_type = 'Interval patterns'
        elif self.mt_fp:
            self.musical_type = 'Form and process'

        # Finalize changes
        super().save()

    def __str__(self):
        return '<{0}> {1}'.format(self.id, self.piece_id)
