from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from crim.helpers.dates import get_date_sort


COMPOSER = 'Composer'


class CRIMRoleType(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Role type'
        verbose_name_plural = 'Role types'

    role_type_id = models.SlugField(
        max_length=32,
        unique=True,
        db_index=True,
    )
    name = models.CharField(max_length=32)
    name_plural = models.CharField(max_length=32, blank=True)
    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    def __str__(self):
        return '{0}'.format(self.name)

    def _get_unique_slug(self):
        slug_base = slugify(self.name)
        unique_slug = slug_base
        num = 1
        while CRIMRoleType.objects.filter(role_type_id=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug_base, num)
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
        on_delete=models.CASCADE,
        to_field='role_type_id',
        blank=True,
        null=True,
        db_index=True,
        related_name='roles',
    )

    date = models.CharField(
        max_length=128,
        blank=True,
        db_index=True,
    )

    date_sort = models.IntegerField(
        null=True
    )

    def person_with_role(self):
        if self.role_type:
            return '{0}, {1}'.format(self.person, str(self.role_type).lower())
        else:
            return self.person
    person_with_role.short_description = 'Role'
    person_with_role.admin_order_field = 'person'

    @property
    def work(self):
        if self.piece:
            return self.piece
        elif self.mass:
            return self.mass
        elif self.treatise:
            return self.treatise
        elif self.source:
            return self.source
        else:  # should not happen after validation
            return None

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

    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    def __str__(self):
        NULL_ROLE_TYPE = 'unknown contributor'
        role_type_to_print = str(self.role_type).lower() if self.role_type else NULL_ROLE_TYPE
        if self.piece:
            return '{0} as {1} of {2}'.format(self.person, role_type_to_print, self.piece)
        elif self.mass:
            return '{0} as {1} of {2}'.format(self.person, role_type_to_print, self.mass)
        elif self.treatise:
            return '{0} as {1} of {2}'.format(self.person, role_type_to_print, self.treatise)
        elif self.source:
            return '{0} as {1} of {2}'.format(self.person, role_type_to_print, self.source)
        else:  # shouldn't happen after validation
            return '{0} as {1}'.format(self.person, role_type_to_print)

    def clean(self):
        number_of_works = ((1 if self.piece else 0) +
                           (1 if self.mass else 0) +
                           (1 if self.treatise else 0) +
                           (1 if self.source else 0)
                           )
        # We allow 0 works to be assigned to a person in order to allow
        # for roles not associated with a work, such as "Bookseller".
        if number_of_works > 1:
            raise ValidationError('You may assign no more than one work to a single role.')

    def save(self, *args, **kwargs):
        self.date_sort = get_date_sort(self.date)

        # Update the related piece
        if self.role_type.name == COMPOSER:
            from crim.models.piece import CRIMPiece
            # Only update the piece or mass if the new date is earlier or equal to the current one
            if self.piece and self.piece.date_sort and self.piece.date_sort >= get_date_sort(self.date):
                self.piece.composer = self.person
                self.piece.date = self.date
                self.piece.date_sort = get_date_sort(self.date)
                self.piece.save()
            elif self.mass:
                if self.mass.date_sort and self.mass.date_sort >= get_date_sort(self.date):
                    self.mass.composer = self.person
                    self.mass.date = self.date
                    self.mass.date_sort = get_date_sort(self.date)
                    self.mass.save()
                for p in CRIMPiece.objects.filter(mass=self.mass):
                    if p.date_sort and p.date_sort >= get_date_sort(self.date):
                        p.composer = self.person
                        p.date = self.date
                        p.date_sort = get_date_sort(self.date)
                        p.save()

        # Finalize changes
        super().save()
