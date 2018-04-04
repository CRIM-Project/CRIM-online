from django.db import models

from crim.models.person import CRIMPerson
from crim.models.role import CRIMRole


class CRIMMass(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Mass'
        verbose_name_plural = 'Masses'

    mass_id = models.CharField(
        max_length=16,
        unique=True,
        primary_key=True,
        db_index=True,
    )
    title = models.CharField(max_length=64, blank=True)
    composer = models.ManyToManyField(
        CRIMPerson,
        through='CRIMRole',
        through_fields=('mass', 'person'),
    )

    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    def creator(self):
        roles = CRIMRole.objects.filter(mass=self).order_by('date_sort')
        if roles:
            return roles[0].person
    creator.short_description = 'creator'

    def date(self):
        roles = CRIMRole.objects.filter(mass=self).order_by('date_sort')
        if roles:
            return roles[0].date_sort
    date.short_description = 'date'

    def __str__(self):
        return '[{0}] {1}'.format(self.mass_id, self.title)
