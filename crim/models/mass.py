from django.db import models
from django.core.exceptions import ValidationError

from crim.helpers.dates import get_date_sort
from crim.models.genre import CRIMGenre
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece
from crim.models.role import CRIMRole
from crim.models.voice import CRIMVoice

import re


class CRIMMass(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Mass'
        verbose_name_plural = 'Masses'

    mass_id = models.CharField(
        'Mass ID',
        max_length=32,
        unique=True,
        db_index=True,
    )
    title = models.CharField(max_length=128)
    genre = models.ForeignKey(
        CRIMGenre,
        on_delete=models.SET_NULL,
        to_field='genre_id',
        default='mass',
        null=True,
    )

    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    # The following data are meant as caches only:
    # they are updated upon save for performance optimization.

    composer = models.ForeignKey(
        CRIMPerson,
        on_delete=models.SET_NULL,
        to_field='person_id',
        null=True,
        db_index=True,
        related_name='masses',
    )
    date = models.CharField(
        max_length=128,
        blank=True,
        db_index=True,
    )
    date_sort = models.IntegerField(
        null=True
    )
    min_number_of_voices = models.IntegerField(
        null=True
    )
    max_number_of_voices = models.IntegerField(
        null=True
    )

    def title_with_id(self):
        return self.__str__()
    title_with_id.short_description = 'mass'
    title_with_id.admin_order_field = 'title'

    @property
    def models(self):
        return CRIMPiece.objects.filter(
                relationships_as_model__derivative_piece__mass=self,
                relationships_as_model__curated=True,
            ).order_by('mass', 'piece_id').select_related(
                'mass',
                'mass__genre',
                'mass__composer',
                'genre',
                'composer',
            ).distinct()

    @property
    def derivatives(self):
        return CRIMPiece.objects.filter(
                relationships_as_derivative__model_piece__mass=self,
                relationships_as_derivative__curated=True,
            ).order_by('mass', 'piece_id').select_related(
                'mass',
                'mass__genre',
                'mass__composer',
                'genre',
                'composer',
            ).distinct()

    def get_absolute_url(self):
        return '/masses/{0}/'.format(self.mass_id)

    def clean(self):
        valid_regex = re.compile(r'^[-_0-9a-zA-Z]+$')
        if not valid_regex.match(self.mass_id):
            raise ValidationError('The Mass ID must consist of letters, numbers, hyphens, and underscores.')

    def save(self, *args, **kwargs):
        # Add number of voices
        list_of_voice_counts = [CRIMVoice.objects.filter(piece=p).count() for p in CRIMPiece.objects.filter(mass=self)]
        self.min_number_of_voices = min(list_of_voice_counts)
        self.max_number_of_voices = max(list_of_voice_counts)

        # Save the composer role with the earliest date associated with this mass
        # in the mass.composer field.
        primary_role = CRIMRole.objects.filter(mass=self, role_type__role_type_id='composer').order_by('date_sort').first()
        self.composer = primary_role.person if primary_role else None
        self.date = primary_role.date if primary_role else ''
        self.date_sort = primary_role.date_sort if primary_role else None

        # Save related pieces as well, which may need roles updated
        for p in CRIMPiece.objects.filter(mass=self):
            p.save()

        super().save()

    def __str__(self):
        return '[{0}] {1}'.format(self.mass_id, self.title)
