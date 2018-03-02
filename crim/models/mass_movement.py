from django.db import models

from crim.models.mass import CRIMMass
from crim import constants


class CRIMMassMovement(CRIMPiece):
    class Meta:
        app_label = "crim"
        verbose_name = "Mass Movement"
        verbose_name_plural = "Mass Movements"

    mass_id = models.ForeignKey(CRIMMass,
                                to_field='id',
                                blank=True,
                                null=True,
                                db_index=True)
    
    def clean(self):
        # Mass movements must be one of five titles.
        if self.title not in MASS_MOVEMENTS:
            raise ValidationError(_('Mass movements must have a title such as "Kyrie" or "Agnus Dei".'))
