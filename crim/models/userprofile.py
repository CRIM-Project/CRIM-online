from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CRIMUserProfile(models.Model):
    class Meta:
        app_label = "crim"

    user = models.OneToOneField(
        User,
        models.CASCADE,
        db_index=True,
    )

#     project_role = models.CharField(max_length=64, blank=True, null=True)
    person = models.ForeignKey(
        'CRIMPerson',
        models.SET_NULL,
        blank=True,
        null=True,
        db_index=True,
        help_text='Link this account with a CRIM Person',
        related_name='profile',
    )

    def __str__(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)

User.profile = property(lambda u: CRIMUserProfile.objects.get_or_create(user=u)[0])
