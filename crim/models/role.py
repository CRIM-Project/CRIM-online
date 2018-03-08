from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# from django.contrib.postgres.fields import ArrayField

from crim.constants import *
from crim.models.person import CRIMPerson


class CRIMRole(models.Model):
    class Meta:
        app_label = "crim"
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    type = models.CharField(max_length=64, choices=ROLE_TYPES, blank=True, db_index=True)

    person = models.ForeignKey(
        CRIMPerson,
        models.CASCADE,
        to_field='person_id',
        db_index=True,
        related_name='roles',
    )

    document_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    document_object_id = models.CharField(max_length=16)
    document = GenericForeignKey('document_content_type', 'document_object_id')
