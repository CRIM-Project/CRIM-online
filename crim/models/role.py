from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify

from crim.constants import *
from crim.models.person import CRIMPerson


class CRIMRoleType(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Role type'
        verbose_name_plural = 'Role types'

    roletype_id = models.SlugField(
        max_length=32,
        unique=True,
        primary_key=True,
        db_index=True,
    )
    name = models.CharField(max_length=32)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return '{0}'.format(self.name)

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while CRIMRoleType.objects.filter(roletype_id=unique_slug).exists():
            slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        # Create unique genre_id based on the name
        if not self.roletype_id:
            self.roletype_id = self._get_unique_slug()
        # Finalize changes
        super().save()


class CRIMRole(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    type = models.ForeignKey(
        CRIMRoleType,
        models.SET_NULL,
        to_field='roletype_id',
        null=True,
        db_index=True,
    )

    person = models.ForeignKey(
        CRIMPerson,
        models.CASCADE,
        to_field='person_id',
        db_index=True,
        related_name='roles',
    )
    
    remarks = models.TextField(blank=True)

    document_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    document_object_id = models.CharField(max_length=16)
    document = GenericForeignKey('document_content_type', 'document_object_id')
