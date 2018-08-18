from django.db import models
from django.contrib.auth.models import User


class CRIMUserProfile(models.Model):
    class Meta:
        app_label = 'crim'
        ordering = ['user__last_name', 'user__first_name', 'user__username']

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_index=True,
    )

    name = models.CharField(max_length=64, db_index=True, blank=True)
    name_sort = models.CharField('sort name (such as ‘Lassus, Orlande de’)', max_length=64, blank=True, db_index=True)

    person = models.ForeignKey(
        'CRIMPerson',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_index=True,
        help_text='Link this account with a CRIM Person',
        related_name='profile',
    )

    @property
    def username(self):
        return self.user.username

    @property
    def username_with_name(self):
        if self.name:
            return '{0} ({1})'.format(self.user.username, self.name)
        else:
            return self.user.username

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.user.username

    def save(self):
        if self.person:
            self.name = self.person.name
            self.name_sort = self.person.name_sort
        else:
            if not self.name:
                self.name = (self.user.first_name + ' ' + self.user.last_name).strip()
            if not self.name_sort:
                self.name_sort = (self.user.last_name + ' ' + self.user.first_name).strip()
        super().save()


User.profile = property(lambda u: CRIMUserProfile.objects.get_or_create(user=u)[0])
