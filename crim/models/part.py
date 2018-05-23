from django.db import models


class CRIMPart(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Part'
        verbose_name_plural = 'Parts'
        ordering = ['part_id']
        unique_together = ('piece', 'order')

    part_id = models.CharField(
        'Part ID',
        max_length=32,
        unique=True,
        db_index=True,
    )

    piece = models.ForeignKey(
        'CRIMPiece',
        on_delete=models.CASCADE,
        to_field='piece_id',
        related_name='parts',
        null=True,
        db_index=True,
    )
    order = models.IntegerField()
    name = models.CharField(max_length=128, blank=True)

    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    def piece_title(self):
        if self.piece.mass:
            return self.piece.mass.title + ': ' + self.piece.title
        else:
            return self.piece.title
    piece_title.short_description = 'piece'

    def save(self):
        if not self.part_id:
            self.part_id = (self.piece.piece_id + '.' + str(self.order))
        super().save()

    def __str__(self):
        # If the part has a name, use it in the string representation
        if self.name:
            return '[{0}] {1} - {2}'.format(self.part_id, self.piece.title, self.name)
        # Otherwise, count how many parts there are for the piece
        # and print the part number if there is more than one
        parts = CRIMPart.objects.filter(piece=self.piece)
        if len(parts) == 1:
            return '[{0}] {1}'.format(self.part_id, self.piece.title)
        else:
            return '[{0}] {1} - Part {2}'.format(self.part_id, self.piece.title, str(self.order))
