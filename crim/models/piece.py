from django.db import models
from django.core.exceptions import ValidationError

from crim.models.genre import CRIMGenre
from crim.models.role import CRIMRole
from crim.models.voice import CRIMVoice

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
        ordering = ['piece_id']

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
    )
    mass = models.ForeignKey(
        'CRIMMass',
        on_delete=models.CASCADE,
        to_field='mass_id',
        related_name='movements',
        null=True,
        db_index=True,
    )
    # This field is redundant with counting the number of voice objects
    # that belong to this piece -- but if those are unknown, we can still
    # fill this in.
    number_of_voices = models.IntegerField(null=True)

    pdf_links = models.TextField('PDF links (one per line)', blank=True)
    mei_links = models.TextField('MEI links (one per line)', blank=True)

    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    def title_with_id(self):
        return self.__str__()
    title_with_id.short_description = 'piece'
    title_with_id.admin_order_field = 'title'

    def composer(self):
        roles = CRIMRole.objects.filter(piece=self, role_type__name=COMPOSER)
        mass_roles = CRIMRole.objects.filter(mass=self.mass, role_type__name=COMPOSER)
        if roles:
            return roles[0].person
        elif mass_roles:
            return mass_roles[0].person
    composer.short_description = 'composer'

    def date(self):
        roles = CRIMRole.objects.filter(piece=self, role_type__name=COMPOSER)
        mass_roles = CRIMRole.objects.filter(mass=self.mass, role_type__name=COMPOSER)
        if roles:
            return roles[0].date_sort
        elif mass_roles:
            return mass_roles[0].date_sort
    date.short_description = 'date'

    def clean(self):
        valid_regex = re.compile(r'^[-_0-9a-zA-Z]+$')
        if self.mass:
            if CRIMPiece.objects.filter(mass=self.mass, title=self.title):
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
            movement_order = dict((x, y) for x, y in self.MASS_MOVEMENT_ORDER)
            self.piece_id = (self.mass.mass_id + '_' + movement_order[self.title])
            # Finally, add the genre Mass to this mass movement.
            self.genre = CRIMGenre.objects.get(genre_id='mass')
        # Remove extraneous newlines from links and voices fields
        self.pdf_links = re.sub(r'[\n\r]+', r'\n', self.pdf_links)
        self.mei_links = re.sub(r'[\n\r]+', r'\n', self.mei_links)

        # Add voice count to the piece. Look at all the voice objects to determine
        # the maximum voice number: if it's greater than the current voice
        # count, update the voice count; otherwise, leave it alone (or null).
        voices = CRIMVoice.objects.filter(piece=self)

        # recursive function using 0 as base case for empty voice list
        def max_voice(voices, current_max=0):
            if not voices:
                return current_max
            else:
                return max_voice(voices[1:], current_max=max(current_max, voices[0].order))

        # get the max number of voices, using the existing number of voices as the minumum
        self.number_of_voices = max_voice(voices, self.number_of_voices if self.number_of_voices else 0)
        # use None instead of 0 if there is no voice count
        if not self.number_of_voices:
            self.number_of_voices = None
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
