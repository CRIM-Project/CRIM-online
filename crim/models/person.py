from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify
from django.utils.html import escape

from crim.helpers.dates import get_date_sort, latest_date
from crim.models.observation import CRIMObservation
from crim.models.relationship import CRIMRelationship
from crim.models.role import CRIMRoleType
import re

ANALYST = 'analyst'


class CRIMPerson(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Person'
        verbose_name_plural = 'People'
        ordering = ['name_sort']

    # Null should be False, because blank values should be stored as empty string.
    person_id = models.CharField('Person ID', max_length=32, unique=True, db_index=True)
    name = models.CharField(max_length=64, db_index=True)
    name_sort = models.CharField('sort name (such as ‘Lassus, Orlande de’)', max_length=64, blank=True, db_index=True)
    # Tried using an array, it was much more trouble than it was worth
    name_alternate_list = models.TextField('list of alternate names (one per line)', blank=True)
    birth_date = models.CharField(max_length=32, blank=True, db_index=True)
    death_date = models.CharField(max_length=32, blank=True, db_index=True)
    active_date = models.CharField(max_length=32, blank=True, db_index=True)
    date_sort = models.IntegerField(null=True)
    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    def sorted_name(self):
        return self.name_sort
    sorted_name.short_description = 'name'
    sorted_name.admin_order_field = 'name_sort'

    def get_absolute_url(self):
        return reverse("crimperson-detail", args=[self.person_id])

    def __str__(self):
        return '{0}'.format(self.name_sort)

    def get_absolute_url(self):
        return '/people/{0}/'.format(self.person_id)

    def save(self, *args, **kwargs):
        # Need to clean `name` field, because its html ends up being parsed!
        self.name = escape(self.name)

        # Add sorted name if it was left blank
        if not self.name_sort:
            self.name_sort = self.name

        # Update integer representation of date
        dates = [self.birth_date, self.death_date, self.active_date]
        self.date_sort = get_date_sort(latest_date(dates))

        # Remove extraneous newlines
        self.name_alternate_list = re.sub(r'[\n\r]+', r'\n', self.name_alternate_list)

        # Finalize changes
        super().save()

    # Return the unique role types associated with this person. If the person
    # has observations or relationships, then we add the Analyst role type.
    @property
    def role_types(self):
        if CRIMObservation.objects.filter(observer=self).exists() or CRIMRelationship.objects.filter(observer=self).exists():
            return CRIMRoleType.objects.filter(Q(roles__person=self) | Q(role_type_id=ANALYST)).distinct()
        else:
            return CRIMRoleType.objects.filter(roles__person=self).distinct()

    @property
    def pieces_analyzed(self):
        from crim.models.piece import CRIMPiece
        return CRIMPiece.objects.filter(
                observations__observer=self,
            ).order_by('mass', 'piece_id').distinct()
