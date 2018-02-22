from django.db import models


class CRIMPerson(models.Model):
    class Meta:
        app_label = "crim"
        verbose_name = "Person"
        verbose_name_plural = "People"
        ordering = ['surname']

    person_id = models.CharField(max_length=16, unique=True, null=True, db_index=True)
    name = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    name_sort = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    name_alternate = models.CharField(max_length=64, blank=True, null=True)
    birth_date = models.CharField(max_length=16, blank=True, null=True)
    death_date = models.CharField(max_length=16, blank=True, null=True)
    active_date = models.CharField(max_length=16, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"{0}".format(self.name)
