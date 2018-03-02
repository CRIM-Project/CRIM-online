from django.db import models
from django.contrib.postgres.fields import ArrayField


class CRIMPerson(models.Model):
    class Meta:
        app_label = "crim"
        verbose_name = "Person"
        verbose_name_plural = "People"
        ordering = ['name_sort']

    # Null should be False, because blank values should be stored as empty string.
    id = models.CharField(max_length=16, unique=True, db_index=True)
    name = models.CharField(max_length=64, blank=True, db_index=True)
    name_sort = models.CharField(max_length=64, blank=True, db_index=True)
    name_alternate_list = ArrayField(models.CharField(max_length=64), blank=True)
    birth_date = models.CharField(max_length=16, blank=True, db_index=True)
    death_date = models.CharField(max_length=16, blank=True, db_index=True)
    active_date = models.CharField(max_length=16, blank=True, db_index=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return u"{0}".format(self.name)
