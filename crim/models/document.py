from django.db import models
from django.core.exceptions import ValidationError

from crim.models.role import CRIMRole

import re

AUTHOR = 'Author'


class CRIMDocument(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        abstract = True

    document_id = models.CharField(
        'Document ID',
        max_length=16,
        unique=True,
        db_index=True,
    )
    title = models.CharField(max_length=64)
    pdf_links = models.TextField('PDF links (one per line)', blank=True)
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

#     people = models.ManyToManyField(
#         CRIMPerson,
#         through='CRIMRole',
#         through_fields=('treatise', 'person'),
#     )

    def author(self):
        roles = CRIMRole.objects.filter(treatise=self, role_type__name=AUTHOR)
        if roles:
            return roles[0].person
    author.short_description = 'author'

    def date(self):
        roles = CRIMRole.objects.filter(treatise=self).order_by('date_sort')
        if roles:
            return roles[0].date_sort
    date.short_description = 'date'


class CRIMSource(CRIMDocument):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Source'
        verbose_name_plural = 'Sources'

#     people = models.ManyToManyField(
#         CRIMPerson,
#         through='CRIMRole',
#         through_fields=('source', 'person'),
#     )

    mass_contents = models.ManyToManyField(
        to='CRIMMass',
        blank=True,
    )
    piece_contents = models.ManyToManyField(
        to='CRIMPiece',
        blank=True,
    )
    treatise_contents = models.ManyToManyField(
        to='CRIMTreatise',
        blank=True,
    )
    source_contents = models.ManyToManyField(
        to='self',
        blank=True,
        symmetrical=False,
    )

    def author(self):
        roles = CRIMRole.objects.filter(source=self, role_type__name=AUTHOR)
        if roles:
            return roles[0].person
    author.short_description = 'author'

    def date(self):
        roles = CRIMRole.objects.filter(source=self).order_by('date_sort')
        if roles:
            return roles[0].date_sort
    date.short_description = 'date'
