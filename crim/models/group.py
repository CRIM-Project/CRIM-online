from django.contrib.auth.models import Group
from django.db import models


class CRIMGroup(Group):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
    public = models.BooleanField(default=False)
