from django.db import models
from django.core.exceptions import ValidationError

from crim.models.role import CRIMRole

import re

AUTHOR = 'author'
PUBLISHER = 'printer'


class CRIMDocument(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        abstract = True

    document_id = models.CharField(
        'Document ID',
        max_length=32,
        unique=True,
        db_index=True,
    )
    title = models.CharField(max_length=128)
    external_links = models.TextField('external links (one per line)', blank=True)
    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    def title_with_id(self):
        return self.__str__()
    title_with_id.short_description = 'document'
    title_with_id.admin_order_field = 'title'

    def clean(self):
        valid_regex = re.compile(r'^[-_0-9a-zA-Z]+$')
        if not valid_regex.match(self.document_id):
            raise ValidationError('The Document ID must consist of letters, numbers, hyphens, and underscores.')

    def __str__(self):
        return '[{0}] {1}'.format(self.document_id, self.title)


class CRIMTreatise(CRIMDocument):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Treatise'
        verbose_name_plural = 'Treatises'

    @property
    def author(self):
        author_roles = CRIMRole.objects.filter(treatise=self, role_type__role_type_id=AUTHOR)
        return author_roles[0].person if author_roles else None

    @property
    def date_sort(self):
        roles = CRIMRole.objects.filter(treatise=self).order_by('date_sort')
        return roles[0].date_sort if roles else None


class CRIMSource(CRIMDocument):
    PRINT = 'print'
    MANUSCRIPT = 'manuscript'
    SOURCE_TYPES = (
        (PRINT, 'Print'),
        (MANUSCRIPT, 'Manuscript'),
    )

    class Meta:
        app_label = 'crim'
        verbose_name = 'Source'
        verbose_name_plural = 'Sources'

    source_type = models.CharField(
        max_length=32,
        choices=SOURCE_TYPES,
        default='PRINT',
    )

    mass_contents = models.ManyToManyField(
        to='CRIMMass',
        blank=True,
        related_name='sources',
    )
    piece_contents = models.ManyToManyField(
        to='CRIMPiece',
        blank=True,
        related_name='sources',
    )
    treatise_contents = models.ManyToManyField(
        to='CRIMTreatise',
        blank=True,
        related_name='sources',
    )

    @property
    def publisher(self):
        publisher_roles = CRIMRole.objects.filter(source=self, role_type__role_type_id=PUBLISHER)
        return publisher_roles[0].person if publisher_roles else None

    @property
    def date_sort(self):
        roles = CRIMRole.objects.filter(source=self).order_by('date_sort')
        return roles[0].date_sort if roles else None
