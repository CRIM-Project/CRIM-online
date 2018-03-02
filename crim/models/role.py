from django.db import models
# from django.contrib.postgres.fields import ArrayField

from crim import constants
from crim.models.person import CRIMPerson
from crim.models.document import CRIMDocument


class CRIMRole(models.Model):
    class Meta:
        app_label = "crim"
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    id = models.CharField(max_length=16, unique=True, db_index=True)
    type = models.CharField(choices=ROLE_TYPES, blank=True, db_index=True)
    person = models.ForeignKey(CRIMPerson, to='id', db_index=True)
    document = models.ForeignKey(CRIMDocument, to='id', db_index=True)

    def __str__(self):
        return u"{0}".format(self.id)
