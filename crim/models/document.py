from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from crim.models.role import CRIMRole


class CRIMDocument(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        abstract = True

    document_id = models.CharField(
        max_length=16,
        unique=True,
        primary_key=True,
        db_index=True,
    )
    title = models.CharField(max_length=64)
    roles = GenericRelation(CRIMRole)
    pdf_link = models.CharField('PDF link', max_length=255, blank=True)
    remarks = models.TextField(blank=True)

    def title_with_id(self):
        return self.__str__()
    title_with_id.short_description = 'document'
    title_with_id.admin_order_field = 'title'

    def __str__(self):
        return '[{0}] {1}'.format(self.document_id, self.title)


class CRIMTreatise(CRIMDocument):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Treatise'
        verbose_name_plural = 'Treatises'

    def creator(self):
        roles = CRIMRole.objects.filter(treatise=self).order_by('date_sort')
        if roles:
            return roles[0].person
    creator.short_description = 'creator'

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

    source_contents = models.ManyToManyField(
        to='self',
        blank=True,
        symmetrical=False,
    )
    treatise_contents = models.ManyToManyField(
        to='CRIMTreatise',
        blank=True,
        symmetrical=False,
    )
    piece_contents = models.ManyToManyField(
        to='CRIMPiece',
        blank=True,
        symmetrical=False,
    )
    mass_contents = models.ManyToManyField(
        to='CRIMMass',
        blank=True,
        symmetrical=False,
    )

    def creator(self):
        roles = CRIMRole.objects.filter(source=self).order_by('date_sort')
        if roles:
            return roles[0].person
    creator.short_description = 'creator'

    def date(self):
        roles = CRIMRole.objects.filter(source=self).order_by('date_sort')
        if roles:
            return roles[0].date_sort
    date.short_description = 'date'
