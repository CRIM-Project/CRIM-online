from django.db import models
from django.core.exceptions import ValidationError

from crim.models.genre import CRIMGenre
from crim.models.role import CRIMRole

import re


COMPOSER = 'Composer'


class CRIMPiece(models.Model):
    # Choices for movement type (used as titles in mass movements)
    EMPTY = ''
    KYRIE = '1'
    GLORIA = '2'
    CREDO = '3'
    SANCTUS = '4'
    AGNUS_DEI = '5'
    MASS_MOVEMENTS = [
        (EMPTY, '---------'),
        (KYRIE, 'Kyrie'),
        (GLORIA, 'Gloria'),
        (CREDO, 'Credo'),
        (SANCTUS, 'Sanctus'),
        (AGNUS_DEI, 'Agnus Dei'),
    ]

    class Meta:
        app_label = 'crim'
        verbose_name = 'Piece'
        verbose_name_plural = 'Pieces'
        ordering = ['piece_id']

    piece_id = models.CharField(
        'Piece ID',
        max_length=16,
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
    )
    mass = models.ForeignKey(
        'CRIMMass',
        on_delete=models.CASCADE,
        to_field='mass_id',
        related_name='movements',
        null=True,
        db_index=True,
    )
#     forces = models.CharField(max_length=16, blank=True)
    pdf_links = models.TextField('PDF links (one per line)', blank=True)
    mei_links = models.TextField('MEI links (one per line)', blank=True)
#     audio_link = models.CharField(max_length=255, blank=True)

    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    def title_with_id(self):
        return self.__str__()
    title_with_id.short_description = 'piece'
    title_with_id.admin_order_field = 'title'

    def composer(self):
        roles = CRIMRole.objects.filter(piece=self, role_type__name=COMPOSER)
        if roles:
            return roles[0].person
    composer.short_description = 'composer'

    def date(self):
        roles = CRIMRole.objects.filter(piece=self, role_type__name=COMPOSER)
        if roles:
            return roles[0].date_sort
    date.short_description = 'date'

    def clean(self):
        valid_regex = re.compile(r'^[-_0-9a-zA-Z]+$')
        if self.mass:
            complete_title = self.mass.title + ': ' + self.title
            if CRIMPiece.objects.filter(mass=self.mass, title=complete_title):
                raise ValidationError('The ' + self.title + ' of ' + self.mass.title + ' already exists.')
        # Only validate Piece ID if it is not a mass movement
        else:
            if not valid_regex.match(self.piece_id):
                raise ValidationError('The Piece ID must consist of letters, numbers, hyphens, and underscores.')

    def save(self):
        # If it is a mass movement, then fill in the Piece ID, title and genre
        if self.mass:
            # `self.title` will be a one-character string ('1', '2', ...)
            # where '1' corresponds to Kyrie, etc.  See the list of
            # constants at the top of the model definition
            self.piece_id = (self.mass.mass_id + '-' + self.title)
            # Add full mass title to the movement type title.
            movement_titles = dict((x, y) for x, y in self.MASS_MOVEMENTS)
            self.title = self.mass.title + ': ' + movement_titles[self.title]
            # Finally, add the genre Mass to this mass movement.
            self.genre = CRIMGenre.objects.get(genre_id='mass')
        # Remove extraneous newlines from links fields
        self.pdf_link = re.sub(r'[\n\r]+', r'\n', self.pdf_link)
        self.mei_link = re.sub(r'[\n\r]+', r'\n', self.mei_link)
        super().save()

    def __str__(self):
        return '[{0}] {1}'.format(self.piece_id, self.title)


class CRIMMassMovement(CRIMPiece):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Mass movement'
        verbose_name_plural = 'Mass movements'
        proxy = True
