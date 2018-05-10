from django.db import models


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

    # This is redundant, but may make indexing easier.
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
    text = models.TextField()
    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    def piece_title(self):
        if self.piece.mass:
            return self.piece.mass.title + ': ' + self.piece.title
        else:
            return self.piece.title
    piece_title.short_description = 'piece'

    def part_name(self):
        return self.part.name
    piece_title.short_description = 'part'

    def save(self):
        if not self.piece:
            self.piece = self.part.piece
        if not self.phrase_id:
            self.phrase_id = (self.piece.piece_id + ':' + str(self.number))
        super().save()

    def __str__(self):
        return '[{0}] {1}, phrase {2}'.format(self.phrase_id, self.piece.title, self.number)
