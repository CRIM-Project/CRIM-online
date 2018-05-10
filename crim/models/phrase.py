from django.db import models
from django.core.exceptions import ValidationError

from crim.models.part import CRIMPart


class CRIMPhrase(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Phrase'
        verbose_name_plural = 'Phrases'
        ordering = ['phrase_id']

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
    # Part number is also redundant, but used in admin to grab the correct part.
    part_number = models.IntegerField('part')
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

    def clean(self):
        if CRIMPhrase.objects.filter(piece=self.piece, number=self.number):
            raise ValidationError("Can't have multiple phrases with the number" + str(self.number))

    def save(self):
        if not self.part:
            matching_parts = CRIMPart.objects.filter(piece=self.piece, order=self.part_number)
            if matching_parts:
                part_to_add = matching_parts[0]
            else:
                part_to_add = CRIMPart(
                    part_id=(self.piece.piece_id + '.' + str(self.part_number)),
                    piece=self.piece,
                    name='',
                    order=self.part_number,
                    remarks='',
                )
                part_to_add.save()
            self.part = part_to_add
        if not self.phrase_id:
            self.phrase_id = (self.piece.piece_id + ':' + str(self.number))
        super().save()

    def __str__(self):
        return '[{0}] {1}, phrase {2}'.format(self.phrase_id, self.piece.title, self.number)
