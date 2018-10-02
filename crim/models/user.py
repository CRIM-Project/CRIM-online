from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


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

@receiver(pre_save, sender=CRIMUserProfile)
def add_name(sender, instance, *args, **kwargs):
    if not instance.name:
        if instance.person:
            instance.name = instance.person.name
        else:
            instance.name = (instance.user.first_name + ' ' + instance.user.last_name).strip()

    if not instance.name_sort:
        if instance.person:
            instance.name_sort = instance.person.name_sort
        else:
            instance.name_sort = (instance.user.last_name + ', ' + instance.user.first_name).strip()


User.profile = property(lambda u: CRIMUserProfile.objects.get(user=u))
