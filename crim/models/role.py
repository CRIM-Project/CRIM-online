from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify


# List of roles:
# AUTHOR = 'author'
# COMPOSER = 'composer'
# EDITOR = 'editor'
# PUBLISHER = 'publisher'
# SCRIBE = 'scribe'
# TRANSLATOR = 'translator'


class CRIMRoleType(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Role type'
        verbose_name_plural = 'Role types'

    role_type_id = models.SlugField(
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
        while CRIMRoleType.objects.filter(role_type_id=unique_slug).exists():
            slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        # Create unique id based on the name
        if not self.role_type_id:
            self.role_type_id = self._get_unique_slug()
        # Finalize changes
        super().save()


class CRIMRole(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    person = models.ForeignKey(
        'CRIMPerson',
        on_delete=models.CASCADE,
        to_field='person_id',
        db_index=True,
        related_name='roles',
    )

    role_type = models.ForeignKey(
        CRIMRoleType,
        on_delete=models.SET_NULL,
        to_field='role_type_id',
        blank=True,
        null=True,
        db_index=True,
    )

    # For implementing using generic foreign keys
#     document_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     document_id = models.CharField(max_length=16)
#     document_object = GenericForeignKey(document_content_type, document_id)

    # Django doesn't make generic foreign keys or many-to-many relations
    # easy, so we have a separate field for each type that could be
    # connected.
    piece = models.ForeignKey(
        'CRIMPiece',
        on_delete=models.CASCADE,
        to_field='piece_id',
        blank=True,
        null=True,
        related_name='roles_as_piece',
    )
    mass = models.ForeignKey(
        'CRIMMass',
        on_delete=models.CASCADE,
        to_field='mass_id',
        blank=True,
        null=True,
        related_name='roles_as_mass',
    )
    treatise = models.ForeignKey(
        'CRIMTreatise',
        on_delete=models.CASCADE,
        to_field='document_id',
        blank=True,
        null=True,
        related_name='roles_as_treatise',
    )
    source = models.ForeignKey(
        'CRIMSource',
        on_delete=models.CASCADE,
        to_field='document_id',
        blank=True,
        null=True,
        related_name='roles_as_source',
    )

    remarks = models.TextField(blank=True)

    def __str__(self):
        NULL_ROLE_TYPE = 'unknown contributor'
        role_type_to_print = str(self.role_type).lower() if self.role_type else NULL_ROLE_TYPE
        if self.piece:
            return '{0} as {1} of {2}'.format(self.person, role_type_to_print, self.piece)
        elif self.mass_movement:
            return '{0} as {1} of {2}'.format(self.person, role_type_to_print, self.mass_movement)
        elif self.mass:
            return '{0} as {1} of {2}'.format(self.person, role_type_to_print, self.mass)
        elif self.treatise:
            return '{0} as {1} of {2}'.format(self.person, role_type_to_print, self.treatise)
        elif self.source:
            return '{0} as {1} of {2}'.format(self.person, role_type_to_print, self.source)
        else:  # shouldn't actually happen
            return '{0} as {1}'.format(self.person, role_type_to_print)
