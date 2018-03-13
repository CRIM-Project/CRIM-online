from django.db import models

from crim.models.document import CRIMDocument
from crim.models.person import CRIMPerson


class CRIMMass(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Mass'
        verbose_name_plural = 'Masses'

    mass_id = models.CharField(
        max_length=16,
        unique=True,
        primary_key=True,
        db_index=True,
    )
    title = models.CharField(max_length=64, blank=True)

    composer = models.ForeignKey(
        CRIMPerson,
        on_delete=models.SET_NULL,
        to_field='person_id',
        db_index=True,
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.composer:
            return '[{0}] {1}: {2}'.format(self.mass_id, self.composer.name, self.title)
        else:
            return '[{0}] Anonymous: {1}'.format(self.mass_id, self.title)
