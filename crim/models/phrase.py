from django.db import models

from crim.helpers.common import two_digit_string


class CRIMPhrase(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Phrase'
        verbose_name_plural = 'Phrases'
        ordering = ['phrase_id']
        unique_together = ('piece', 'number')

    phrase_id = models.CharField(
        'Phrase ID',
        max_length=32,
        unique=True,
        db_index=True,
    )

    # This is redundant (because we also have `part`),
    # but may make indexing easier.
    piece = models.ForeignKey(
        'CRIMPiece',
        on_delete=models.CASCADE,
        to_field='piece_id',
        related_name='phrases',
        null=True,
        db_index=True,
    )
    part = models.ForeignKey(
        'CRIMPart',
        on_delete=models.CASCADE,
        to_field='part_id',
        related_name='phrases',
        null=True,
        db_index=True,
    )
    number = models.IntegerField('phrase number')
    start_measure = models.IntegerField(null=True)
    stop_measure = models.IntegerField(null=True)
    text = models.TextField(blank=True)
    translation = models.TextField(blank=True)
    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    def piece_title(self):
        if self.piece.mass:
            return self.piece.mass.title + ': ' + self.piece.title
        else:
            return self.piece.title
    piece_title.short_description = 'piece'

    def part_number(self):
        return self.part.order
    part_number.short_description = 'part'

    def save(self):
        if not self.piece:
            self.piece = self.part.piece
        if not self.phrase_id:
            self.phrase_id = (self.piece.piece_id + ':' + two_digit_string(self.number))
        super().save()

    def __str__(self):
        return '[{0}] {1}, phrase {2}'.format(self.phrase_id, self.piece.title, self.number)
