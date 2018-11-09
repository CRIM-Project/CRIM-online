from django.db import models
from django.core.exceptions import ValidationError

from crim.common import get_date_sort
from crim.models.genre import CRIMGenre
from crim.models.piece import CRIMPiece
from crim.models.role import CRIMRole

import re

COMPOSER = 'Composer'


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

    def title_with_id(self):
        return self.__str__()
    title_with_id.short_description = 'mass'
    title_with_id.admin_order_field = 'title'

    @property
    def composer(self):
        composer_roles = CRIMRole.objects.filter(mass=self, role_type__name=COMPOSER)
        return composer_roles[0].person if composer_roles else None

    @property
    def date_sort(self):
        composer_roles = CRIMRole.objects.filter(mass=self, role_type__name=COMPOSER)
        return get_date_sort(composer_roles[0].date) if composer_roles else None

    @property
    def models(self):
        return CRIMPiece.objects.filter(
                relationships_as_model__derivative_piece__mass=self,
                relationships_as_model__curated=True,
            ).order_by('mass', 'piece_id').distinct()

    @property
    def derivatives(self):
        return CRIMPiece.objects.filter(
                relationships_as_derivative__model_piece__mass=self,
                relationships_as_derivative__curated=True,
            ).order_by('mass', 'piece_id').distinct()

    def save(self, *args, **kwargs):
        super().save()

    def clean(self):
        valid_regex = re.compile(r'^[-_0-9a-zA-Z]+$')
        if not valid_regex.match(self.mass_id):
            raise ValidationError('The Mass ID must consist of letters, numbers, hyphens, and underscores.')

    def __str__(self):
        return '[{0}] {1}'.format(self.mass_id, self.title)
