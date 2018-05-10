from django.db import models
from django.core.exceptions import ValidationError

import re


class CRIMVoice(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Voice'
        verbose_name_plural = 'Voices'
        ordering = ['voice_id']

    voice_id = models.CharField(
        'Voice ID',
        max_length=32,
        unique=True,
        db_index=True,
    )

    piece = models.ForeignKey(
        'CRIMPiece',
        on_delete=models.CASCADE,
        to_field='piece_id',
        related_name='voices',
        null=True,
        db_index=True,
    )
    name = models.CharField(max_length=128)
    order = models.IntegerField()
    supplied = models.BooleanField(default=False)
    clef = models.CharField(max_length=8, blank=True)

    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    def piece_title(self):
        if self.piece.mass:
            return self.piece.mass.title + ': ' + self.piece.title
        else:
            return self.piece.title
    piece_title.short_description = 'piece'

    def clean(self):
        valid_clef_regex = re.compile(r'^([CFG]-[1-5])?$')
        if not valid_clef_regex.match(self.clef):
            raise ValidationError('Clef must be in the format ‘C-4’.')

    def save(self):
        if not self.voice_id:
            self.voice_id = (self.piece.piece_id + '(' + str(self.order) + ')')
        super().save()

    def __str__(self):
        return '[{0}] {1} ({2})'.format(self.voice_id, self.piece.title, self.name)
