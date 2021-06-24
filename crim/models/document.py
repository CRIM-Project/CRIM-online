from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError

from crim.models.person import CRIMPerson
from crim.models.role import CRIMRole

import re


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

    # The following data are meant as caches only:
    # they are updated upon save for performance optimization.

    date = models.CharField(
        max_length=128,
        blank=True,
        db_index=True,
    )
    date_sort = models.IntegerField(
        null=True
    )

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

    # The following is meant as a cache, containing redundant data
    # for performance reasons.

    author = models.ForeignKey(
        CRIMPerson,
        on_delete=models.SET_NULL,
        to_field='person_id',
        null=True,
        db_index=True,
        related_name='treatises',
    )

    def get_absolute_url(self):
        return '/treatises/{0}/'.format(self.document_id)

    def save(self):
        # Remove extraneous newlines from external_links field
        self.external_links = re.sub(r'[\n\r]+', r'\n', self.external_links)

        # Save the author role with the earliest date associated with this piece
        # in the document.author field.
        primary_role = CRIMRole.objects.filter(treatise=self, role_type__role_type_id='author').order_by('date_sort').first()
        self.author = primary_role.person if primary_role else None
        self.date = primary_role.date if primary_role else ''
        self.date_sort = primary_role.date_sort if primary_role else None

        super().save()


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

    # The following is meant as a cache, containing redundant data
    # for performance reasons.

    publisher = models.ForeignKey(
        CRIMPerson,
        on_delete=models.SET_NULL,
        to_field='person_id',
        null=True,
        db_index=True,
        related_name='sources',
    )

    def get_absolute_url(self):
        return '/sources/{0}/'.format(self.document_id)

    def save(self):
        # Remove extraneous newlines from external_links field
        self.external_links = re.sub(r'[\n\r]+', r'\n', self.external_links)

        # Save the printer or scribe role (whichever is applicable) with the
        # earliest date associated with this piece in the document.publisher field.
        primary_role = CRIMRole.objects.get(source=self, Q(role_type__role_type_id='scribe') | Q(role_type__role_type_id='printer')).order_by('date_sort').first()
        self.publisher = primary_role.person if primary_role else None
        self.date = primary_role.date if primary_role else ''
        self.date_sort = primary_role.date_sort if primary_role else None

        super().save()
