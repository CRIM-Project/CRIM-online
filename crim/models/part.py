from django.db import models
from django.core.exceptions import ValidationError


class CRIMPart(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Part'
        verbose_name_plural = 'Parts'
        ordering = ['part_id']

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
    name = models.CharField(max_length=128)
    order = models.IntegerField()

    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    def piece_title(self):
        if self.piece.mass:
            return self.piece.mass.title + ': ' + self.piece.title
        else:
            return self.piece.title
    piece_title.short_description = 'piece'

    def clean(self):
        if CRIMPart.objects.filter(piece=self.piece, order=self.order):
            raise ValidationError('Part ' + self.name + ' of ' + self.piece.title + ' already exists.')
        if CRIMPart.objects.filter(piece=self.piece, order=self.order):
            raise ValidationError('Part ' + str(self.order) + ' of ' + self.piece.title + ' already exists.')

    def save(self):
        if not self.part_id:
            self.part_id = (self.piece.piece_id + '.' + str(self.order))
        super().save()

    def __str__(self):
        return '[{0}] {1} - {2}'.format(self.part_id, self.piece.title, self.name)
