import re

from django.core.cache import caches
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from crim.helpers.common import cache_values_to_string
from crim.helpers.dates import get_date_sort
from crim.models.genre import CRIMGenre
from crim.models.person import CRIMPerson
from crim.models.role import CRIMRole, CRIMRoleType
from crim.models.voice import CRIMVoice


# This decorator is for not trying to cache things imported as fixture.
def disable_for_loaddata(signal_handler):
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs['raw']:
            return
        signal_handler(*args, **kwargs)
    return wrapper


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

    # The following data are meant as caches only:
    # they are updated upon save for performance optimization.

    full_title = models.CharField(
        max_length=128,
        blank=True,
        db_index=True,
    )
    composer = models.ForeignKey(
        CRIMPerson,
        on_delete=models.SET_NULL,
        to_field='person_id',
        null=True,
        db_index=True,
        related_name='pieces',
    )
    date = models.CharField(
        max_length=128,
        blank=True,
        db_index=True,
    )
    date_sort = models.IntegerField(
        null=True
    )
    number_of_voices = models.IntegerField(
        null=True
    )

    def title_with_id(self):
        return self.__str__()

    title_with_id.short_description = 'piece'
    title_with_id.admin_order_field = 'title'

    @property
    def models(self):
        return CRIMPiece.objects.filter(
                relationships_as_model__derivative_piece=self,
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
                relationships_as_derivative__model_piece=self,
                relationships_as_derivative__curated=True,
            ).order_by('mass', 'piece_id').select_related(
                'mass',
                'mass__genre',
                'mass__composer',
                'genre',
                'composer',
            ).distinct()

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
            self.full_title = self.mass.title + ': ' + self.title
            movement_order = dict((x, y) for x, y in self.MASS_MOVEMENT_ORDER)
            self.piece_id = (self.mass.mass_id + '_' + movement_order[self.title])
            # Add the genre Mass to this mass movement.
            self.genre = CRIMGenre.objects.get(genre_id='mass')
        else:
            self.full_title = self.title
        # Add number of voices
        self.number_of_voices = CRIMVoice.objects.filter(piece=self).count()
        # Remove extraneous newlines from links and voices fields
        self.pdf_links = re.sub(r'[\n\r]+', r'\n', self.pdf_links)
        self.mei_links = re.sub(r'[\n\r]+', r'\n', self.mei_links)

        # Save the composer role with the earliest date associated with this piece
        # in the piece.composer field.
        primary_role = CRIMRole.objects.filter(piece=self, role_type__role_type_id='composer').order_by('date_sort').first()
        # Get the information from the related mass if necessary
        if not primary_role and self.mass:
            primary_role = CRIMRole.objects.filter(mass=self.mass, role_type__role_type_id='composer').order_by('date_sort').first()

        if primary_role:
            self.composer = primary_role.person
            self.date = primary_role.date
            self.date_sort = primary_role.date_sort
        else:
            self.composer = None
            self.date = ''
            self.date_sort = None

        super().save()

    def __str__(self):
        return '[{0}] {1}'.format(self.piece_id, self.full_title)


@receiver(post_save, sender=CRIMPiece)
def update_piece_cache(sender, instance=None, created=None, **kwargs):
    # Cache the notation for this piece
    if instance and not kwargs.get('raw', True):  # So that this does not run when importing fixture
        from crim.views.piece import render_piece
        print('Caching {}'.format(instance.piece_id))
        for i in range(30):
            render_piece(instance.piece_id, i+1)


@receiver(post_delete, sender=CRIMPiece)
def delete_piece_cache(sender, instance=None, **kwargs):
    from django.core.cache import caches
    print('Deleting cache for {}'.format(instance.piece_id))
    for i in range(30):
        caches['pieces'].delete(cache_values_to_string(instance.piece_id, i+1))


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
