from django.db import models

from crim.models.mass import CRIMMass
from crim.models.piece import CRIMPiece
from crim.models.genre import CRIMGenre


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

    def save(self):
        self.genre = CRIMGenre(genre_id='mass')
        # TODO: Needs validation that title is one of the following:
        # Kyrie, Gloria, Credo, Sanctus, Agnus Dei
        super().save()
