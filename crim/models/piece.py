from django.db import models
from django.core.exceptions import ValidationError

from crim.common import get_date_sort
from crim.models.genre import CRIMGenre
from crim.models.role import CRIMRole

import re


COMPOSER = 'Composer'


class CRIMPiece(models.Model):
    # Choices for movement type (used as titles in mass movements)
    EMPTY = ''
    KYRIE = 'Kyrie'
    GLORIA = 'Gloria'
    CREDO = 'Credo'
    SANCTUS = 'Sanctus'
    AGNUS_DEI = 'Agnus Dei'
    MASS_MOVEMENTS = [
        (EMPTY, '---------'),
        (KYRIE, 'Kyrie'),
        (GLORIA, 'Gloria'),
        (CREDO, 'Credo'),
        (SANCTUS, 'Sanctus'),
        (AGNUS_DEI, 'Agnus Dei'),
    ]
    MASS_MOVEMENT_ORDER = (
        ('Kyrie', '1'),
        ('Gloria', '2'),
        ('Credo', '3'),
        ('Sanctus', '4'),
        ('Agnus Dei', '5'),
    )

    class Meta:
        app_label = 'crim'
        verbose_name = 'Piece'
        verbose_name_plural = 'Pieces'
        ordering = ['mass', 'piece_id']
        unique_together = ('mass', 'title')

    piece_id = models.CharField(
        'Piece ID',
        max_length=32,
        unique=True,
        db_index=True,
    )
    title = models.CharField(max_length=128)
    genre = models.ForeignKey(
        CRIMGenre,
        on_delete=models.SET_NULL,
        to_field='genre_id',
        null=True,
        db_index=True,
        related_name='pieces',
    )
    mass = models.ForeignKey(
        'CRIMMass',
        on_delete=models.CASCADE,
        to_field='mass_id',
        related_name='movements',
        null=True,
        db_index=True,
    )

    pdf_links = models.TextField('PDF links (one per line)', blank=True)
    mei_links = models.TextField('MEI links (one per line)', blank=True)

    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    def title_with_id(self):
        return self.__str__()
    title_with_id.short_description = 'piece'
    title_with_id.admin_order_field = 'title'

    @property
    def composer(self):
        composer_roles = CRIMRole.objects.filter(piece=self, role_type__name=COMPOSER)
        mass_composer_roles = CRIMRole.objects.filter(mass=self.mass, role_type__name=COMPOSER)
        if composer_roles:
            return composer_roles[0].person
        elif mass_composer_roles:
            return mass_composer_roles[0].person
        else:
            return None

    @property
    def date_sort(self):
        composer_roles = CRIMRole.objects.filter(piece=self, role_type__name=COMPOSER)
        mass_composer_roles = CRIMRole.objects.filter(mass=self.mass, role_type__name=COMPOSER)
        if composer_roles:
            return get_date_sort(composer_roles[0].date)
        elif mass_composer_roles:
            return get_date_sort(mass_composer_roles[0].date)
        else:
            return None

    @property
    def models(self):
        return CRIMPiece.objects.filter(
                relationships_as_model__derivative_piece=self,
                relationships_as_model__curated=True,
            ).order_by('mass', 'piece_id').distinct()

    @property
    def derivatives(self):
        return CRIMPiece.objects.filter(
                relationships_as_derivative__model_piece=self,
                relationships_as_derivative__curated=True,
            ).order_by('mass', 'piece_id').distinct()

    def get_absolute_url(self):
        return '/pieces/{0}/'.format(self.piece_id)

    def clean(self):
        valid_regex = re.compile(r'^[-_0-9a-zA-Z]+$')
        # Only validate Piece ID if it is not a mass movement
        if not self.mass and not valid_regex.match(self.piece_id):
            raise ValidationError('The Piece ID must consist of letters, numbers, hyphens, and underscores.')

    def save(self):
        # If it is a mass movement, then fill in the Piece ID, title and genre
        if self.mass:
            # `self.title` will be a one-character string ('1', '2', ...)
            # where '1' corresponds to Kyrie, etc.  See the list of
            # constants at the top of the model definition
            movement_order = dict((x, y) for x, y in self.MASS_MOVEMENT_ORDER)
            self.piece_id = (self.mass.mass_id + '_' + movement_order[self.title])
            # Finally, add the genre Mass to this mass movement.
            self.genre = CRIMGenre.objects.get(genre_id='mass')
        # Remove extraneous newlines from links and voices fields
        self.pdf_links = re.sub(r'[\n\r]+', r'\n', self.pdf_links)
        self.mei_links = re.sub(r'[\n\r]+', r'\n', self.mei_links)

        super().save()

    def __str__(self):
        if not self.mass:
            return '[{0}] {1}'.format(self.piece_id, self.title)
        else:
            return '[{0}] {1}: {2}'.format(self.piece_id, self.mass.title, self.title)


class CRIMModel(CRIMPiece):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Piece: Model'
        verbose_name_plural = 'Pieces: Models'
        proxy = True


class CRIMMassMovement(CRIMPiece):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Piece: Mass movement'
        verbose_name_plural = 'Pieces: Mass movements'
        proxy = True
