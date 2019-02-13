from django.contrib.auth.models import Group
from django.db import models


class CRIMGroup(Group):
    public = models.BooleanField(default=False)
