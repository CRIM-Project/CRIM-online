from django.db import models
from django.contrib.postgres.fields import ArrayField

from crim import constants
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece


class CRIMPiece(CRIMDocument):
    class Meta:
        app_label = "crim"
        verbose_name = "Relationship"
        verbose_name_plural = "Relationships"

    id = models.CharField(max_length=16, unique=True, db_index=True)
    observer_id = models.ForeignKey(CRIMPerson, to='id', db_index=True)
    relationship_type = models.CharField(
        choices=RELATIONSHIP_TYPES,
        blank=True,
        db_index=True
    )
    
    model_id = models.ForeignKey(CRIMPiece, to='id', db_index=True)
    model_ema = models.CharField()
    model_musical_types = ArrayField( 
        models.CharField(choices=MUSICAL_TYPES),
        blank=True
    )
    
    
    derivative_id = models.ForeignKey(CRIMPiece, to='id', db_index=True)
    derivative_ema = models.CharField()
    
#     forces = models.CharField(max_length=16, blank=True)
    pdf_link = models.CharField(max_length=255, blank=True)
    mei_link = models.CharField(max_length=255, blank=True)
#     audio_link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"{0}".format(self.id)
