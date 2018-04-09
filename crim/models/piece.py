from django.db import models
from django.core.exceptions import ValidationError

from crim.models.genre import CRIMGenre
from crim.models.person import CRIMPerson
from crim.models.mass import CRIMMass
from crim.models.role import CRIMRole

import re
from dateutil.parser import parse


class CRIMPiece(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Piece'
        verbose_name_plural = 'Pieces'

    piece_id = models.CharField(
        'Piece ID',
        max_length=16,
        unique=True,
        primary_key=True,
        db_index=True,
    )
#     people = models.ManyToManyField(
#         CRIMPerson,
#         through='CRIMRole',
#         through_fields=('piece', 'person'),
#     )
    title = models.CharField(max_length=64)
    genre = models.ForeignKey(
        CRIMGenre,
        on_delete=models.SET_NULL,
        to_field='genre_id',
        null=True,
        db_index=True,
    )

#     forces = models.CharField(max_length=16, blank=True)
    pdf_link = models.CharField('PDF link', max_length=255, blank=True)
    mei_link = models.CharField('MEI link', max_length=255, blank=True)
#     audio_link = models.CharField(max_length=255, blank=True)

    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    def title_with_id(self):
        return self.__str__()
    title_with_id.short_description = 'piece'
    title_with_id.admin_order_field = 'title'

    def creator(self):
        roles = CRIMRole.objects.filter(piece=self).order_by('date_sort')
        if roles:
            return roles[0].person
    creator.short_description = 'creator'

    def date(self):
        roles = CRIMRole.objects.filter(piece=self).order_by('date_sort')
        if roles:
            return roles[0].date_sort
    date.short_description = 'date'

    def clean(self):
        valid_regex = re.compile(r'^[-_0-9a-zA-Z]+$')
        if not valid_regex.match(self.piece_id):
            raise ValidationError('The Piece ID must consist of letters, numbers, hyphens, and underscores.')

    def __str__(self):
        return '[{0}] {1}'.format(self.piece_id, self.title)


class CRIMMassMovement(CRIMPiece):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Mass Movement'
        verbose_name_plural = 'Mass Movements'

    mass = models.ForeignKey(
        CRIMMass,
        on_delete=models.SET_NULL,
        to_field='mass_id',
        null=True,
        db_index=True,
        related_name='movements',
    )

    def __str__(self):
        return '[{0}] {1}: {2}'.format(self.piece_id, self.mass.title, self.title)

    def mass_date(self):
        return self.mass.date()
    mass_date.short_description = 'Date'
