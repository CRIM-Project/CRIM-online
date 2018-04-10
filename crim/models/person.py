from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from django.utils.html import escape
import re

from dateutil.parser import parse


class CRIMPerson(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Person'
        verbose_name_plural = 'People'
        ordering = ['name_sort']

    # Null should be False, because blank values should be stored as empty string.
    person_id = models.SlugField(max_length=64, unique=True, primary_key=True, db_index=True)
    name = models.CharField(max_length=64, db_index=True)
    name_sort = models.CharField('sort name (such as ‘Lassus, Orlande de’)', max_length=64, blank=True, db_index=True)
    # Tried using an array, it was much more trouble than it was worth
    name_alternate_list = models.TextField('list of alternate names, each on a new line', blank=True)
    birth_date = models.CharField(max_length=32, blank=True, db_index=True)
    death_date = models.CharField(max_length=32, blank=True, db_index=True)
    active_date = models.CharField(max_length=32, blank=True, db_index=True)
    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    date_sort = models.IntegerField(null=True)

    def sorted_name(self):
        return self.name_sort
    sorted_name.short_description = 'name'
    sorted_name.admin_order_field = 'name_sort'

    def sorted_date(self):
        return self.date_sort
    sorted_date.short_description = 'date'
    sorted_date.admin_order_field = 'date_sort'

    def __str__(self):
        return '{0}'.format(self.name)

    def _get_unique_slug(self):
        slug_base = slugify(self.name)
        unique_slug = slug_base
        num = 1
        while CRIMPerson.objects.filter(person_id=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug_base, num)
            num += 1
        return unique_slug

    def _get_date_sort(self):
        try:
            birth_date_parsed = parse(self.birth_date, fuzzy=True).year
        except ValueError:
            birth_date_parsed = 0
        try:
            death_date_parsed = parse(self.death_date, fuzzy=True).year
        except ValueError:
            death_date_parsed = 0
        try:
            active_date_parsed = parse(self.active_date, fuzzy=True).year
        except ValueError:
            active_date_parsed = 0
        return max(birth_date_parsed, death_date_parsed, active_date_parsed)

    def save(self, *args, **kwargs):
        # Create unique person_id based on the name
        if not self.person_id:
            self.person_id = self._get_unique_slug()

        # Need to clean `name` field, because its html ends up being parsed!
        self.name = escape(self.name)

        # Add sorted name if it was left blank
        if not self.name_sort:
            self.name_sort = self.name

        # Add sortable date field based on birth, death and active dates
        if self._get_date_sort() == 0:
            self.date_sort = None
        else:
            self.date_sort = self._get_date_sort()

        # Remove extraneous newlines
        self.name_alternate_list = re.sub(r'[\n\r]+', r'\n', self.name_alternate_list)

        # Finalize changes
        super().save()
