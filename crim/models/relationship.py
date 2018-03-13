from django.db import models
from django.contrib.postgres.fields import ArrayField

from crim.constants import *
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece


class CRIMRelationship(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Relationship'
        verbose_name_plural = 'Relationships'

    relationship_id = models.CharField(
        max_length=16,
        unique=True,
        db_index=True,
    )

    observer = models.ForeignKey(
        CRIMPerson,
        models.SET_NULL,
        to_field='person_id',
        null=True,
        db_index=True,
        related_name='relationships',
    )

    relationship_type = models.CharField(
        max_length=64,
        choices=RELATIONSHIP_TYPES,
        blank=True,
        null=True,
        db_index=True,
    )
    
    model = models.ForeignKey(
        CRIMPiece,
        models.CASCADE,
        to_field='piece_id',
        db_index=True,
        related_name='relationships_as_model',
    )
    model_ema = models.TextField()
    model_musical_types = ArrayField( 
        models.CharField(max_length=64, choices=MUSICAL_TYPES),
        blank=True
    )
    
    derivative = models.ForeignKey(
        CRIMPiece,
        models.CASCADE,
        to_field='piece_id',
        db_index=True,
        related_name='relationships_as_derivative',
    )
    derivative_ema = models.TextField()
    
#     forces = models.CharField(max_length=16, blank=True)
    pdf_link = models.CharField(max_length=255, blank=True)
    mei_link = models.CharField(max_length=255, blank=True)
#     audio_link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return '{0}'.format(self.relationship_id)
