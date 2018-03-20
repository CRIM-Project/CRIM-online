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
    remarks = models.TextField(blank=True)
    roles = GenericRelation(CRIMRole)

    def __str__(self):
        return '{0}: {1}'.format(self.document_id, self.title)


class CRIMTreatise(CRIMDocument):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Treatise'
        verbose_name_plural = 'Treatises'

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
    
    contents = models.ManyToManyField(
        to='self',
        blank=True,
        symmetrical=False,
    )

    def date(self):
        roles = CRIMRole.objects.filter(source=self).order_by('date_sort')
        if roles:
            return roles[0].date_sort
    date.short_description = 'date'
