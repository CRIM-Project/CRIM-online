from django.db import models

from crim.models.person import CRIMPerson
from crim.models.genre import CRIMGenre
from crim.constants import *

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
    title = models.CharField(max_length=64)
    genre = models.ForeignKey(
        CRIMGenre,
        models.SET_NULL,
        to_field='genre_id',
        null=True,
        db_index=True,
    )
    date_of_composition = models.CharField(max_length=32, blank=True, db_index=True)
    date_sort = models.IntegerField(null=True)

#     forces = models.CharField(max_length=16, blank=True)
    pdf_link = models.CharField('PDF link', max_length=255, blank=True)
    mei_link = models.CharField('MEI link', max_length=255, blank=True)
#     audio_link = models.CharField(max_length=255, blank=True)
    
    def sorted_date(self):
        return self.date_sort
    sorted_date.short_description = 'date'
    sorted_date.admin_order_field = 'date_sort'

    def __str__(self):
        return '[{0}] {1}'.format(self.piece_id, self.title)

    def _get_date_sort(self):
        try:
            date_parsed = parse(self.date_of_composition, fuzzy=True).year
        except ValueError:
            date_parsed = 0
        return date_parsed

    def save(self, *args, **kwargs):
        # Add sortable date field
        if self._get_date_sort() == 0:
            self.date_sort = None
        else:
            self.date_sort = self._get_date_sort()
        # Finalize changes
        super().save()
