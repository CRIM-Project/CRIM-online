from django.core.management.base import BaseCommand
from crim.models.role import CRIMRole


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for role in CRIMRole.objects.all():
            role.save()
