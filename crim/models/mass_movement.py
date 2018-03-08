from django.db import models

from crim.models.mass import CRIMMass
from crim.models.piece import CRIMPiece
from crim.constants import *


class CRIMMassMovement(CRIMPiece):
    class Meta:
        app_label = "crim"
        verbose_name = "Mass Movement"
        verbose_name_plural = "Mass Movements"

    mass = models.ForeignKey(
        CRIMMass,
        models.SET_NULL,
        to_field='mass_id',
        null=True,
        db_index=True,
        related_name='movements',
    )
