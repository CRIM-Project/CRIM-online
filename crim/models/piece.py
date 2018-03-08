from django.db import models

from crim.models.person import CRIMPerson
from crim.constants import *


class CRIMPiece(models.Model):
    class Meta:
        app_label = "crim"
        verbose_name = "Piece"
        verbose_name_plural = "Pieces"
    
    piece_id = models.CharField(max_length=16, unique=True, primary_key=True, db_index=True)
    title = models.CharField(max_length=64, blank=True)
    genre = models.CharField(max_length=64, blank=True, choices=GENRES)

    composer = models.ForeignKey(
        CRIMPerson,
        models.SET_NULL,
        to_field='person_id',
        db_index=True,
        blank=True,
        null=True,
    )

#     forces = models.CharField(max_length=16, blank=True)
    pdf_link = models.CharField(max_length=255, blank=True)
    mei_link = models.CharField(max_length=255, blank=True)
#     audio_link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return '[{0}] {1}'.format(self.piece_id, self.title)
