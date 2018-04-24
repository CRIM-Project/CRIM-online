from django.db import models

from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece


class CRIMObservation(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Observation'
        verbose_name_plural = 'Observations'

    observation_id = models.SlugField(
        'observation ID',
        max_length=32,
        unique=True,
    )

    observer = models.ForeignKey(
        CRIMPerson,
        on_delete=models.SET_NULL,
        to_field='person_id',
        null=True,
        db_index=True,
        related_name='observations',
    )

    piece = models.ForeignKey(
        CRIMPiece,
        on_delete=models.CASCADE,
        to_field='piece_id',
        db_index=True,
        related_name='observations',
    )
    ema = models.TextField('EMA expression', blank=True)

    mt_cf_voice = models.CharField('voice', max_length=16, blank=True)
    mt_cf_dur = models.BooleanField('durations only', default=False)
    mt_cf_mel = models.BooleanField('intervals only', default=False)
    mt_sog_voice = models.CharField('voice', max_length=16, blank=True)
    mt_sog_dur = models.BooleanField('durations only', default=False)
    mt_sog_mel = models.BooleanField('intervals only', default=False)
    mt_sog_ostinato = models.BooleanField('ostinato', default=False)
    mt_sog_periodic = models.BooleanField('periodic', default=False)
    mt_csog_voice = models.CharField('voice', max_length=16, blank=True)
    mt_csog_dur = models.BooleanField('durations only', default=False)
    mt_csog_mel = models.BooleanField('intervals only', default=False)
    mt_cd_voice1 = models.CharField('voice 1', max_length=16, blank=True)
    mt_cd_voice2 = models.CharField('voice 2', max_length=16, blank=True)
    mt_fg_voice1 = models.CharField('voice 1', max_length=16, blank=True)
    mt_fg_voice2 = models.CharField('voice 2', max_length=16, blank=True)
    mt_fg_voice3 = models.CharField('voice 3', max_length=16, blank=True)
    mt_fg_voice4 = models.CharField('voice 4', max_length=16, blank=True)
    mt_fg_periodic = models.BooleanField('periodic', default=False)
    mt_fg_strict = models.BooleanField('strict', default=False)
    mt_fg_flexed = models.BooleanField('flexed', default=False)
    mt_fg_sequential = models.BooleanField('sequential', default=False)
    mt_fg_inverted = models.BooleanField('inverted', default=False)
    mt_fg_retrograde = models.BooleanField('retrograde', default=False)
    mt_fg_int = models.CharField('intervals', max_length=32, blank=True)  # better name?
    mt_fg_tint = models.CharField('tint', max_length=32, blank=True)  # needs better name
    mt_id_voice1 = models.CharField('voice 1', max_length=16, blank=True)
    mt_id_voice2 = models.CharField('voice 2', max_length=16, blank=True)
    mt_id_voice3 = models.CharField('voice 3', max_length=16, blank=True)
    mt_id_voice4 = models.CharField('voice 4', max_length=16, blank=True)
    mt_id_strict = models.BooleanField('strict', default=False)
    mt_id_flexed = models.BooleanField('flexed', default=False)
    mt_id_flt = models.BooleanField('flexed tonal', default=False)
    mt_id_sequential = models.BooleanField('sequential', default=False)
    mt_id_added = models.BooleanField('added', max_length=32, blank=True)
    mt_id_invertible = models.BooleanField('invertible', default=False)
    mt_id_int = models.CharField('intervals', max_length=32, blank=True)  # better name?
    mt_id_tint = models.CharField('tint', max_length=32, blank=True)  # needs better name
    mt_pe_voice1 = models.CharField('voice 1', max_length=16, blank=True)
    mt_pe_voice2 = models.CharField('voice 2', max_length=16, blank=True)
    mt_pe_voice3 = models.CharField('voice 3', max_length=16, blank=True)
    mt_pe_strict = models.BooleanField('strict', default=False)
    mt_pe_flexed = models.BooleanField('flexed', default=False)
    mt_pe_flt = models.BooleanField('flexed tonal', default=False)
    mt_pe_sequential = models.BooleanField('sequential', default=False)
    mt_pe_added = models.BooleanField('added', default=False)
    mt_pe_invertible = models.BooleanField('invertible', default=False)
    mt_pe_int = models.CharField('intervals', max_length=32, blank=True)  # better name?
    mt_pe_tint = models.CharField('tint', max_length=32, blank=True)  # needs better name
    mt_nid_voice1 = models.CharField('voice 1', max_length=16, blank=True)
    mt_nid_voice2 = models.CharField('voice 2', max_length=16, blank=True)
    mt_nid_voice3 = models.CharField('voice 3', max_length=16, blank=True)
    mt_nid_strict = models.BooleanField('strict', default=False)
    mt_nid_flexed = models.BooleanField('flexed', default=False)
    mt_nid_flt = models.BooleanField('flexed tonal', default=False)
    mt_nid_sequential = models.BooleanField('sequential', default=False)
    mt_nid_invertible = models.BooleanField('invertible', default=False)
    mt_nid_int = models.CharField('intervals', max_length=32, blank=True)  # better name?
    mt_nid_tint = models.CharField('tint', max_length=32, blank=True)  # needs better name
    mt_hr_voice1 = models.CharField('voice 1', max_length=16, blank=True)
    mt_hr_voice2 = models.CharField('voice 2', max_length=16, blank=True)
    mt_hr_voice3 = models.CharField('voice 3', max_length=16, blank=True)
    mt_hr_simple = models.BooleanField('simple', default=False)
    mt_hr_staggered = models.BooleanField('staggered', default=False)
    mt_hr_sequential = models.BooleanField('sequential', default=False)
    mt_hr_fauxbourdon = models.BooleanField('fauxbourdon', default=False)
    mt_cad_voice1 = models.CharField('voice 1', max_length=16, blank=True)
    mt_cad_voice2 = models.CharField('voice 2', max_length=16, blank=True)
    mt_cad_authentic = models.BooleanField('voice 3', default=False)
    mt_cad_phrygian = models.BooleanField('phrygian', default=False)
    mt_cad_plagal = models.BooleanField('plagal', default=False)
    mt_cad_tone = models.CharField('tone', max_length=4, blank=True)
    mt_cad_dtv = models.CharField('dovetail voice', max_length=32, blank=True)
    mt_cad_dti = models.CharField('interval', max_length=32, blank=True)
    mt_int_voice1 = models.CharField('voice 1', max_length=16, blank=True)
    mt_int_voice2 = models.CharField('voice 2', max_length=16, blank=True)
    mt_int_p6 = models.BooleanField('parallel 6', default=False)
    mt_int_p3 = models.BooleanField('parallel 3 (or 10)', default=False)
    mt_int_c35 = models.BooleanField('chained 3 and 5', default=False)
    mt_int_c83 = models.BooleanField('chained 8 and 3', default=False)
    mt_int_c65 = models.BooleanField('chained 6 and 5', default=False)
    mt_fp_comment = models.TextField('comment', blank=True)
    mt_fp_ir = models.BooleanField('internal repetition', default=False)
    mt_fp_range = models.CharField('range', max_length=16, blank=True)

    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    needs_review = models.BooleanField(default=False)

    def __str__(self):
        return '{0}'.format(self.relationship_id)

    def _get_unique_slug(self):
        slug_base = self.piece.piece_id
        num = 1
        unique_slug = '{}-{}'.format(slug_base, num)
        while CRIMObservation.objects.filter(relationship_id=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug_base, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        # Create unique id based on the `piece_id` of the piece involved
        if not self.relationship_id:
            self.relationship_id = self._get_unique_slug()
        # Finalize changes
        super().save()
